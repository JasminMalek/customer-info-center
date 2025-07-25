<template>
  <div class="row">
    <div class="col-12 mt-2 mb-2 text-end">
      <router-link :to="{ name: 'ticketAdd' }" class="btn btn-primary">Create New Ticket</router-link>
    </div>
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <h4>Support Tickets</h4>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Title</th>
                  <th>Customer</th>
                  <th>Product</th>
                  <th>Priority</th>
                  <th>Status</th>
                  <th>Jira Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <template v-if="!loading">
                <tbody v-if="tickets.length > 0">
                  <tr v-for="(ticket, key) in tickets" :key="key">
                    <td>{{ ticket.id }}</td>
                    <td>{{ ticket.title }}</td>
                    <td>{{ ticket.customer_name || 'N/A' }}</td>
                    <td>
                      <span v-if="ticket.product_name" class="badge bg-info">
                        {{ ticket.product_name }}
                      </span>
                      <span v-else class="badge bg-danger">No Product</span>
                    </td>
                    <td>
                      <span :class="getPriorityClass(ticket.priority)">
                        {{ ticket.priority }}
                      </span>
                    </td>
                    <td>{{ ticket.status }}</td>
                    <td>
                      <span v-if="ticket.jira_synced" class="badge bg-success">
                        {{ ticket.jira_issue_key }}
                      </span>
                      <span v-else class="badge bg-warning">Not Synced</span>
                    </td>
                    <td>
                      <router-link :to="{ name: 'ticketEdit', params: { id: ticket.id } }" 
                                   class="btn btn-sm btn-success me-1">Edit</router-link>
                      <router-link :to="{ name: 'ticketShow', params: { id: ticket.id } }" 
                                   class="btn btn-sm btn-primary me-1">View</router-link>
                      <button v-if="!ticket.jira_synced && ticket.product_id" 
                              @click="syncToJira(ticket.id)" 
                              class="btn btn-sm btn-info me-1"
                              :disabled="syncingTickets.includes(ticket.id)">
                        <i v-if="syncingTickets.includes(ticket.id)" class="fa fa-spinner fa-spin"></i>
                        {{ syncingTickets.includes(ticket.id) ? 'Syncing...' : 'Send to Jira' }}
                      </button>
                      <button v-if="!ticket.product_id" 
                              class="btn btn-sm btn-warning me-1" 
                              disabled
                              title="Product must be assigned before syncing to Jira">
                        Link Product First
                      </button>
                      <button type="button" @click="deleteTicket(ticket.id)" 
                              class="btn btn-sm btn-danger">Delete</button>
                    </td>
                  </tr>
                </tbody>
                <tbody v-else>
                  <tr>
                    <td colspan="8" align="center">No Tickets Found.</td>
                  </tr>
                </tbody>
              </template>
              <tbody v-else>
                <tr>
                  <td colspan="8" class="text-center">
                    <i class="fa fa-spinner fa-spin"></i> Loading...
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Jira Sync Status Modal -->
  <div class="modal fade" id="jiraSyncModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ syncResult.success ? 'Sync Successful' : 'Sync Failed' }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div v-if="syncResult.success" class="alert alert-success">
            <i class="fa fa-check-circle"></i>
            <strong>Success!</strong> {{ syncResult.message }}
            <br><br>
            <strong>Jira Issue Key:</strong> {{ syncResult.jira_issue_key }}
          </div>
          <div v-else class="alert alert-danger">
            <i class="fa fa-exclamation-triangle"></i>
            <strong>Error:</strong> {{ syncResult.error }}
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TicketList",
  data() {
    return {
      tickets: [],
      loading: true,
      syncingTickets: [],
      syncResult: {
        success: false,
        message: '',
        error: '',
        jira_issue_key: ''
      }
    };
  },
  mounted() {
    this.axios = axios;
    this.getTickets();
  },
  methods: {
    async getTickets() {
      try {
        const response = await this.axios.get('http://localhost:5000/tickets');
        this.tickets = response.data;
      } catch (error) {
        console.error('Error fetching tickets:', error);
        this.tickets = [];
        alert('Failed to load tickets');
      } finally {
        this.loading = false;
      }
    },
    
    async syncToJira(ticketId) {
      // Validate that ticket has product before syncing
      const ticket = this.tickets.find(t => t.id === ticketId);
      if (!ticket.product_id) {
        alert('Failed to sync to Jira - Ticket must be linked to a product.');
        return;
      }
      
      this.syncingTickets.push(ticketId);
      
      try {
        const response = await this.axios.post(`http://localhost:5000/tickets/${ticketId}/sync-to-jira`);
        
        this.syncResult = {
          success: true,
          message: response.data.message,
          jira_issue_key: response.data.jira_issue_key,
          error: ''
        };
        
        // Update the ticket in the list
        const ticketIndex = this.tickets.findIndex(t => t.id === ticketId);
        if (ticketIndex !== -1) {
          this.tickets[ticketIndex].jira_synced = true;
          this.tickets[ticketIndex].jira_issue_key = response.data.jira_issue_key;
        }
        
        // Show success modal
        const modal = new bootstrap.Modal(document.getElementById('jiraSyncModal'));
        modal.show();
        
      } catch (error) {
        console.error('Error syncing to Jira:', error);
        
        this.syncResult = {
          success: false,
          error: error.response?.data?.error || 'Unknown error occurred',
          message: '',
          jira_issue_key: ''
        };
        
        // Show error modal
        const modal = new bootstrap.Modal(document.getElementById('jiraSyncModal'));
        modal.show();
        
      } finally {
        this.syncingTickets = this.syncingTickets.filter(id => id !== ticketId);
      }
    },
    
    async deleteTicket(id) {
      const confirmed = window.confirm("Are you sure you want to delete this ticket?");
      if (confirmed) {
        try {
          await this.axios.delete(`http://localhost:5000/tickets/${id}`);
          alert('Ticket deleted successfully');
          await this.getTickets(); // Refresh the list
        } catch (error) {
          console.error('Error deleting ticket:', error);
          alert('Failed to delete ticket');
        }
      }
    },
    
    getPriorityClass(priority) {
      const classes = {
        'High': 'badge bg-danger',
        'Medium': 'badge bg-warning',
        'Low': 'badge bg-success'
      };
      return classes[priority] || 'badge bg-secondary';
    }
  }
};
</script>

<style scoped>
.badge {
  font-size: 0.8rem;
}

.btn-sm {
  margin-right: 2px;
}

.table td {
  vertical-align: middle;
}

.alert {
  margin-bottom: 0;
}

.fa {
  margin-right: 5px;
}
</style>