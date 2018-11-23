<template>
  <div id="home-wrapper"></div>
</template>

<script>
import '@/plugins/socketio.js'
export default {
  name: 'home',
  data () { return {} },
  sockets: {
    connect () {
    },
    disconnect () {
    },
    status (data) {
      this.$notify({
        title: data.title,
        message: this.$createElement('i', { style: 'color: teal' }, data.message)
      })
    },
    realtime (data) {
    }
  }
}
</script>
