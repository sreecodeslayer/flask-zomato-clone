<template>
  <el-row style="background-color: teal">
    <el-col :span="24">
      <el-header style="padding: 0">
        <el-row>
          <el-col :span="21">
            <!-- Navs -->
            <el-menu :default-active="activeIndex" background-color="teal" text-color="white" router mode="horizontal"  active-text-color="yellow" style="border-bottom: none;background-color: transparent;">
              <el-menu-item index="1" :route="{path:'/'}">Home</el-menu-item>
              <el-menu-item index="2" :route="{path:'/tasks'}">Tasks</el-menu-item>
            </el-menu>
          </el-col>
          <el-col :span="3" style="height: 60px">
            <!-- Notification/Logout buttons -->
            <el-menu :default-active="activeIndex"  text-color="white" router mode="horizontal"  active-text-color="yellow" style="border-bottom: none;background-color: transparent;">
              <el-menu-item index="3" :route="{path:'/'}">
                <el-badge is-dot class="item" v-if="hasTasks"><i class="el-icon-bell" style="color: yellow" /></el-badge>
                <i v-else class="el-icon-bell" style="color: white" />
              </el-menu-item>
              <el-menu-item index="4"><i class="el-icon-d-arrow-right"  style="color: white" @click="$auth.logout()"/></el-menu-item>
            </el-menu>
          </el-col>
        </el-row>
      </el-header>
    </el-col>
  </el-row>
</template>
<style>
  .el-badge__content.is-fixed.is-dot {
    margin-top: 10px
  }

</style>
<script>
export default {
  name: 'NavBar',
  data () {
    return {
      activeIndex: '1',
      hasTasks: false
    }
  },
  sockets: {
    realtime (data) {
      this.hasTasks = data.status
    }
  }
}
</script>
