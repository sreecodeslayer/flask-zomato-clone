let loadUser = function () {
  try {
    return JSON.parse(window.localStorage.user)
  } catch (e) {
    return null
  }
}

export default loadUser
