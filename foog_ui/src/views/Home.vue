<template>
  <div id="home-wrapper">
    <el-row>
      <el-col :span="24"></el-col>
    </el-row>
    <el-row  :gutter="24" v-if="valet">
      <el-col :span="20">
        <el-table :data="tasks.results" style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="scope">
              <h4>History</h4>
              <span v-for="his in scope.row.history">
                <p><el-tag size="medium" type="success">{{ his.status }}</el-tag>&nbsp;(Updated {{his.made_at | humanizeTime}})</p>
              </span>
            </template>
          </el-table-column>
          <el-table-column label="Title" prop="title"></el-table-column>
          <el-table-column label="Current Status" prop="status"></el-table-column>
          <el-table-column label="Priority">
            <template slot-scope="scope">
              <el-tag size="medium" v-if="scope.row.priority === 'low'" type="warning">{{ scope.row.priority }}</el-tag>
              <el-tag size="medium" v-if="scope.row.priority === 'medium'" type="primary">{{ scope.row.priority }}</el-tag>
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
              <el-dropdown @command="handlePatchStatus">
                <span class="el-dropdown-link">
                  Change status<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item disabled>Accept</el-dropdown-item>
                  <el-dropdown-item :disabled="scope.row.status === 'completed'" :command="{status:'declined',id:scope.row.id}">Decline</el-dropdown-item>
                  <el-dropdown-item :disabled="scope.row.status === 'completed'" :command="{status:'completed',id:scope.row.id}">Complete</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col :span="4">
        <h4>Updates</h4>
        <el-card shadow="always" v-if="updated" style="color: deeppink">
          <div slot="header">
            <span>Task!
              <el-button style="float: right; padding: 5px" type="success" @click="getNewTask">View</el-button>
            </span>
          </div>
          <i class="el-icon-info"></i>&nbsp;A new task is available
        </el-card>
        <p v-else>No tasks available</p>
      </el-col>
    </el-row>
    <el-row  :gutter="24" v-if="manager">
      <el-col :span="20">
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
                    <p><el-tag size="medium" type="success">{{ his.status }}</el-tag>&nbsp;(Updated {{his.made_at | humanizeTime}})</p>
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
                  <el-button size="small" type="danger" icon="el-icon-delete" circle @click="deleteTask(scope.row.id)"></el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover">
          <h4>New task</h4>
          <el-form ref="newTaskForm" label-position="top"  :model="newTaskForm" @submit.native.prevent="addNewTask">
            <el-form-item label="Title">
              <el-input v-model="newTaskForm.title" placeholder="Task title here"></el-input>
            </el-form-item>
            <el-form-item label="Priority">
              <el-select v-model="newTaskForm.priority">
                <el-option label="Low" value="low"></el-option>
                <el-option label="Medium" value="medium"></el-option>
                <el-option label="High" value="high"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="success" native-type="submit">Add</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <!-- Dialogs -->
    <el-dialog  :visible.sync="newJobDialog.value" width="30%" :close-on-click-modal="false" :show-close="false" :close-on-press-escape="false" v-if="valet && (newJobDialog.data.id || newJobDialog.errs)">
      <div v-if="!newJobDialog.errs">
        <span><h2>{{newJobDialog.data.title}}</h2></span>
        <p>Manager: {{newJobDialog.data.created_by.username}}({{newJobDialog.data.created_by.email}})</p>
        <p>Created on: {{newJobDialog.data.created_on | calendarTime}}</p>
        <p>Priority:
          <el-tag size="medium" v-if="newJobDialog.data.priority === 'low'" type="warning">{{ newJobDialog.data.priority }}</el-tag>
          <el-tag size="medium" v-if="newJobDialog.data.priority === 'medium'" type="info">{{ newJobDialog.data.priority }}</el-tag>
          <el-tag size="medium" v-if="newJobDialog.data.priority === 'high'" type="danger">{{ newJobDialog.data.priority }}</el-tag>
        </p>
        <span slot="footer" class="dialog-footer">
          <el-button type="danger" @click="newJobDialog.value= false;patchStatus('declined',newJobDialog.data.id)">Decline</el-button>
          <el-button type="success" @click="newJobDialog.value= false;patchStatus('accepted',newJobDialog.data.id)">Accept</el-button>
        </span>
      </div>
      <div v-else>
        <span><el-alert title="Job fetch error" type="error" :description="newJobDialog.errs" :show-icon="false"></el-alert></span>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import '@/plugins/socketio.js'
import loadUser from '@/utils'
export default {
  name: 'home',
  data () {
    return {
      activeTabName: 'current',
      eligible: false,
      updated: false,
      statusUpdateId: '',
      newJobDialog: { value: false, data: {}, errs: '' },
      manager: false,
      valet: false,
      tasks: {
        pagination: { page: 1, total: 0, totalPages: 0, perPage: 10 },
        results: []
      },
      newTaskForm: {
        title: '',
        priority: ''
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
  computed: {
    activeTasks () {
      return this.tasks.results.filter((task) => (task.status === 'accepted'))
    }
  },
  methods: {
    handlePatchStatus (cmd) {
      this.patchStatus(cmd.status, cmd.id)
    },
    getNewTask () {
      let url = '/api/v1/valets/job'
      this.$http.get(url).then(
        (response) => {
          this.newJobDialog.value = true
          this.newJobDialog.data = response.data
        },
        (err) => {
          this.newJobDialog.value = true
          this.newJobDialog.errs = err.response.data.message
        })
    },
    addNewTask () {
      let url = '/api/v1/jobs'

      this.$http.post(url, this.newTaskForm).then(
        (response) => {
          this.tasks.results.push(response.data)
        },
        (err) => {})
    },
    deleteTask (id) {
      let url = '/api/v1/jobs/' + id
      this.$http.delete(url).then((response) => {
        this.fetchTasks()
      }, (err) => {})
    },
    patchStatus (status, id) {
      let url = '/api/v1/jobs/' + id + '/status'
      this.$http.patch(url, { status: status }).then((response) => {
        this.fetchTasks()
      },
      (err) => {
        console.log(err)
      })
    },
    fetchTasks () {
      let url = ''

      if (this.valet) {
        url = '/api/v1/valets/deliveries' +
          '?page=' + this.tasks.pagination.page +
          '&perPage=' + this.tasks.pagination.perPage
      } else {
        url = '/api/v1/jobs' +
          '?page=' + this.tasks.pagination.page +
          '&perPage=' + this.tasks.pagination.perPage
      }

      console.log(url)

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
  created () {
    // window.addEventListener('beforeunload', (e) => {
    //   // This might not work on page reloads depending on if user has interacted with user
    //   // https://developer.mozilla.org/en-US/docs/Web/Events/beforeunload#Notes
    //   if (this.newJob) {
    //     e.preventDefault()
    //     e.returnvalue = 'Seems like you have not updated a pending job approval, decline it?'
    //   }
    // })
    this.user = loadUser()
    this.manager = this.user.roles.includes('manager')
    this.valet = !this.manager
    this.fetchTasks()
  },
  ready () {
  }
  // beforeRouteLeave (to, from, next) {
  //   let user = loadUser()
  //   if (!user.roles.includes('manager')) {
  //     this.$router.push('/tasks')
  //   } else {
  //     if (this.newJob) {
  //       this.$alert(
  //         'Seems like you have not updated a pending job approval, decline it?',
  //         'Notice',
  //         {
  //           confirmButtonText: 'OK',
  //           showClose: false,
  //           type: 'error',
  //           callback: action => {
  //             next()
  //           }
  //         }
  //       )
  //     }
  //   }
  // }

}
</script>
