'use strict';

(function () {
  let intervalId
  let timeoutId

  const config = {
    check: {
      intervalTimeout: 5000
    },
    typing: {
      intervalTimeout: 1000
    },
    inputs: {
      from: 'input-translate-from',
      to: 'input-translate-to'
    },
    api: {
      check: '/check',
      previous: '/previous',
      schedule: '/schedule'
    }
  }

  const api = {
    fetch: function (uri, func, params, onError) {
      return axios.get(uri, params)
        .then(func)
        .catch(function (error) {
          events.logError(error)

          if (onError) {
            onError()
          }
        })
    }
  }

  const events = {
    attach: function (element, eventName, func) {
      if (!element) {
        return
      }

      element.addEventListener(eventName, func)
    },
    debounce: function (timeoutId, timeout, func) {
      window.clearTimeout(timeoutId)
      timeoutId = window.setTimeout(func, timeout)

      return timeoutId
    },
    logError: function (error) {
      const message = error.response && error.response.data && error.response.data.message
        ? error.response.data.message
        : error.message

      console.error('[log]', message)
    }
  }

  const createParameter = function (value) {
    return value
      ? {
          params: {
            value: window.encodeURIComponent(value)
          }
        }
      : null
  }

  const checkTranslation = function (uid) {
    const uidParameter = createParameter(uid)

    intervalId = window.setInterval(function () {
      api.fetch(config.api.check, function (response) {
        const translated = response.data.translated
        const inputFrom = document.getElementById(config.inputs.from)
        const inputTo = document.getElementById(config.inputs.to)

        // translated !!
        if (translated) {
          // Clear future interval
          window.clearInterval(intervalId)

          // Update translated value
          inputTo.value = translated

          // Remove blocking state
          inputFrom.removeAttribute('disabled')

          // Retrieve previous translations
          previousTranslations()
        }
      }, uidParameter, function () {
        // Clear future interval
        window.clearInterval(intervalId)
      })
    }, config.check.intervalTimeout)
  }

  const scheduleTranslation = function (target) {
    const translationParameter = createParameter(target.value)

    api.fetch(config.api.schedule, function (response) {
      checkTranslation(response.data.uid)
    }, translationParameter, function () {
      const inputFrom = document.getElementById(config.inputs.from)

      // Remove blocking state
      inputFrom.removeAttribute('disabled')
    })
  }

  const previousTranslations = function () {
    api.fetch(config.api.previous, function (response) {
      const ul = document.getElementById('list-previous')
      const previousList = response.data
      let li = ul.children[0].cloneNode()

      if (!previousList || !previousList.length) {
        return
      }

      let childrens = previousList.map(function (item) {
        li.innerHTML = `${item.from_text} => ${item.to_text}`

        return li.outerHTML
      }).join('')

      // should update dom?
      if (ul.innerHTML !== childrens) {
        ul.innerHTML = childrens
      }
    })
  }

  // DOM Loaded
  events.attach(document, 'DOMContentLoaded', function () {
    const inputFrom = document.getElementById(config.inputs.from)

    events.attach(inputFrom, 'keypress', function (event) {
      const target = event.target

      timeoutId = events.debounce(timeoutId, config.typing.intervalTimeout, function () {
        // if empty, do not proceed
        if (!target.value) {
          return
        }

        const inputTo = document.getElementById(config.inputs.to)

        inputTo.value = ''

        target.disabled = true

        scheduleTranslation(target)
      })
    })

    events.attach(inputFrom, 'blur', function (event) {
      if (!event.target.value) {
        const inputTo = document.getElementById(config.inputs.to)

        inputTo.value = ''
      }
    })

    previousTranslations()
  })
})()
