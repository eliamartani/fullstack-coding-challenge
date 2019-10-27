'use strict';

(function () {
  let typingTimerId
  const typingTimerTimeout = 500

  const attachEvent = function (element, eventName, fn) {
    if (!element) {
      return
    }

    element.addEventListener(eventName, fn)
  }

  const debounceTyping = function (event) {
    const target = event.target

    window.clearTimeout(typingTimerId)

    typingTimerId = window.setTimeout(function () {
      // call api here
      console.log(target.value)
    }, typingTimerTimeout)
  }

  attachEvent(
    document.getElementById('input-translate-from'),
    'keypress',
    debounceTyping
  )
})()
