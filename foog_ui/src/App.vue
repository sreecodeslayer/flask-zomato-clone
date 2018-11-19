<template>
 <div id="app" v-if="!$route.meta.public">
    <!-- Main pages -->
    <router-view/>
  </div>
  <div id="app" v-else style="height='100%'">
    <!-- Login, Signup, About pages -->
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
    }
  },
  sockets: {
    connect () {
      console.log('connected')
    },
    disconnect () {
      console.log('disconnected')
    },
    status (data) {
      this.$notify({
        title: data.title,
        message: this.$createElement('i', { style: 'color: teal' }, data.message)
      })
    }
  },
  created () {
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.text-xs {
  font-size: 12px;
}
.text-sm {
  font-size: 13px;
}
.text-md {
  font-size: 14px;
}
.text-lg {
  font-size: 16px;
}

</style>
