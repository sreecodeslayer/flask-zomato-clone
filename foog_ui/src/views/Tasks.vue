<template>
  <div id="tasks-wrapper">
    <el-tabs v-model="activeTabName">
      <el-tab-pane label="Active Tasks" name="current">
        {{activeTasks}}
      </el-tab-pane>
      <el-tab-pane :label="'Previous Tasks ( '+tasks.results.length+' )'" name="previous">
        {{tasks.results}}
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<style></style>
<script>
export default{
  name: 'tasks',
  data () {
    return {
      activeTabName: 'current',
      tasks: {
        pagination: { page: 1, total: 0, totalPages: 0, perPage: 10 },
        results: []
      }
    }
  },
  computed: {
    activeTasks () {
      return this.tasks.results.filter((task) => (task.status === 'accepted'))
    }
  },
  sockets: {
    realtime (data) {}
  },
  methods: {
    fetchTasks () {
      let url = '/api/v1/jobs' +
      '?page=' + this.tasks.pagination.page +
      '&perPage=' + this.tasks.pagination.perPage

      this.$http.get(url).then(
        (response) => {
          this.tasks.results = response.data.results
          this.tasks.pagination.totalPages = response.data.total_pages
          this.tasks.pagination.total = response.data.total
        },
        (err) => {

        }
      )
    }
  },
  mounted () {
    this.fetchTasks()
  }
}
</script>
