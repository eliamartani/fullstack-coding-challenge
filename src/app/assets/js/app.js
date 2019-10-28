'use strict';

(function () {
  let checkApiId
  let typingTimerId
  const checkApiTimeout = 2000
  const typingTimerTimeout = 1000

  const attachEvent = function (element, eventName, fn) {
    if (!element) {
      return
    }

    element.addEventListener(eventName, fn)
  }

  const clearInput = function (event) {
    if (!event.target.value) {
      document.getElementById('input-translate-to').value = ''
    }
  }

  const debounceTyping = function (event) {
    const target = event.target

    window.clearTimeout(typingTimerId)

    typingTimerId = window.setTimeout(function () {
      // if empty, do not proceed
      if (!target.value) {
        return
      }

      target.disabled = true

      scheduleTranslation(target)
    }, typingTimerTimeout)
  }

  const fetchApi = function (uri, fn, value) {
    const params = value
      ? {
          params: {
            'value': window.encodeURIComponent(value)
          }
        }
      : null

    axios.get(uri, params).then(fn).catch(logError)
  }

  const logError = function (error) {
    const message = error.response && error.response.data && error.response.data.message
      ? error.response.data.message
      : error.message

    console.error('[log]', message)
  }

  const scheduleTranslation = function (target) {
    const inputTo = document.getElementById('input-translate-to')

    inputTo.value = '...'

    fetchApi('/schedule', function (response) {
      const uid = response.data.uid

      checkApiId = window.setInterval(function () {
        fetchApi('/check', function (response) {
          const translated = response.data.translated

          // translated !!
          if (translated) {
            // Clear future interval
            window.clearInterval(checkApiId)

            // Update translated value
            inputTo.value = translated

            // Remove blocking state
            target.removeAttribute('disabled')

            // Retrieve previous translations
            previousTranslations()
          }
        }, uid)
      }, checkApiTimeout)
    }, target.value)
  }

  const previousTranslations = function () {
    fetchApi('/previous', function (response) {
      const ul = document.getElementById('list-previous')
      const list = response.data
      let li = ul.children[0].cloneNode()

      if (!list.length) {
        return
      }

      let childrens = list.map(function (text) {
        li.innerHTML = text

        return li.outerHTML
      }).join('')

      // should update dom?
      if (ul.innerHTML !== childrens) {
        ul.innerHTML = childrens
      }
    })
  }

  // dom loaded
  attachEvent(
    document,
    'DOMContentLoaded',
    function () {
      const inputFrom = document.getElementById('input-translate-from')

      if (inputFrom) {
        // keypress for input
        attachEvent(inputFrom, 'keypress', debounceTyping)
        attachEvent(inputFrom, 'blur', clearInput)
      }

      previousTranslations()
    }
  )
})()
