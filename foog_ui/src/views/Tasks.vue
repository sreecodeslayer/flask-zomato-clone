<template>
  <div id="tasks-wrapper">
    <el-tabs v-model="activeTabName">
      <el-tab-pane label="Active Tasks" name="current">
        {{activeTasks}}
      </el-tab-pane>
      <el-tab-pane :label="'Previous Tasks ( '+tasks.results.length+' )'" name="previous">
        <el-table :data="tasks.results" style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="scope">
              <h4>History</h4>
              <span v-for="his in scope.row.history">
                <el-tag size="medium" type="success">{{ his.status }}</el-tag>&nbsp;(Updated {{his.made_at | humanizeTime}})
              </span>
            </template>
          </el-table-column>
          <el-table-column label="Title" prop="title"></el-table-column>
          <el-table-column label="Current Status" prop="status"></el-table-column>
          <el-table-column label="Priority">
            <template slot-scope="scope">
              <el-tag size="medium" v-if="scope.row.priority === 'low'" type="warning">{{ scope.row.priority }}</el-tag>
              <el-tag size="medium" v-if="scope.row.priority === 'medium'" type="info">{{ scope.row.priority }}</el-tag>
              <el-tag size="medium" v-if="scope.row.priority === 'high'" type="danger">{{ scope.row.priority }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="Created on">
            <template slot-scope="scope">
              {{scope.row.created_on | calendarTime}}
            </template>
          </el-table-column>
          <el-table-column label="Action">
            <template slot-scope="scope">
                <el-button size="small" type="danger" icon="el-icon-delete" circle @click></el-button>
            </template>
          </el-table-column>
        </el-table>
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
