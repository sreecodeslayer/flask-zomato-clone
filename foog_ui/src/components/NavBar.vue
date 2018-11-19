<template>
  <el-header>
    <el-menu :default-active="activeIndex"  text-color="grey" router mode="horizontal"  active-text-color="teal">
      <el-menu-item index="1" :route="{path:'/'}">Home</el-menu-item>
      <el-submenu index="2">
        <template slot="title">Tasks</template>
        <el-menu-item index="2-1" :route="{path:'/tasks/new'}">New</el-menu-item>
        <el-menu-item index="2-2" :route="{path:'/tasks'}">All Tasks</el-menu-item>
      </el-submenu>
    </el-menu>
  </el-header>
</template>
<style></style>
<script>
export default {
  name: 'NavBar',
  data () {
    return {

      activeIndex: '1'
    }
  }
}
</script>
