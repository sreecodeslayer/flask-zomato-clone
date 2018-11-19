<template>
 <div id="app" v-if="!$route.meta.public">
  <!-- Main pages -->
  <el-container id="main-container" style="height: calc(92vh);">
  <nav-bar/>
    <el-main>
      <router-view/>
    </el-main>
    <el-footer></el-footer>
  </el-container>
</div>
<div id="app" v-else style="height='100%'">
  <!-- Login, Signup, About pages -->
  <router-view/>
</div>
</template>

<script>
import NavBar from '@/components/NavBar'
export default {
  name: 'app',
  components: { NavBar },
  data () {
    return {

      activeIndex: '1'
    }
  },
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
  },
  created () {
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
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
