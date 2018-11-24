<template>
  <div id="home-wrapper">
    <el-row>
      <el-col :span="24"></el-col>
    </el-row>
    <el-row  :gutter="24">
      <el-col :span="20">
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
      </el-col>
      <el-col :span="4">
        <h4>Updates</h4>
        <el-card shadow="hover" v-if="eligible && updated">
          <i class="el-icon-info"></i>A new task is available
        </el-card>
        <p v-else>No tasks available</p>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import '@/plugins/socketio.js'
export default {
  name: 'home',
  data () {
    return {
      eligible: false,
      updated: false,
      tasks: {
        pagination: { page: 1, total: 0, totalPages: 0, perPage: 10 },
        results: []
      }
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
      this.updated = data.status
    }
  },
  methods: {
    fetchMyTasks () {
      let url = '/api/v1/valets/deliveries' +
        '?page=' + this.tasks.pagination.page +
        '&perPage=' + this.tasks.pagination.perPage

      this.$http.get(url).then(
        (response) => {
          this.tasks.results = response.data.results
          this.tasks.pagination.totalPages = response.data.total_pages
          this.tasks.pagination.total = response.data.total
        },
        (err) => {
          if (err.response.status === 403) {
            this.$alert('Seems like you are accessing Delivery tasks details.\nYou have been logged out.\nPlease login back into delivery account', 'Oops!', {
              confirmButtonText: 'OK',
              showClose: false,
              type: 'error',
              callback: action => {
                this.$socket.disconnect()
                this.$auth.logout()
                window.location = '/'
              }
            })
          }
        }
      )
    }
  },
  created () {
    this.fetchMyTasks()
  }
}
</script>
