<template>
    <div class="row mt-1">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h4>Create New Ticket</h4>
                </div>
                <div class="card-body">
                    <form @submit.prevent="submitTicket">
                        <div class="row">
                            <div class="col-12 mb-3">
                                <div class="form-group">
                                    <label>Ticket Title <span class="text-danger">*</span></label>
                                    <input type="text" 
                                           class="form-control" 
                                           v-model="ticket.title" 
                                           required
                                           placeholder="Enter ticket title">
                                </div>
                            </div>
                            
                            <div class="col-6 mb-3">
                                <div class="form-group">
                                    <label>Customer <span class="text-danger">*</span></label>
                                    <select class="form-control" v-model="ticket.customer_id" required>
                                        <option value="">Select Customer</option>
                                        <option v-for="customer in customers" 
                                                :key="customer.id" 
                                                :value="customer.id">
                                            {{ customer.name }}
                                        </option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="col-6 mb-3">
                                <div class="form-group">
                                    <label>Product <span class="text-danger">*</span></label>
                                    <select class="form-control" v-model="ticket.product_id" required>
                                        <option value="">Select Product</option>
                                        <option v-for="product in products" 
                                                :key="product.id" 
                                                :value="product.id">
                                            {{ product.name }}
                                            <span v-if="product.jira_project_key">({{ product.jira_project_key }})</span>
                                        </option>
                                    </select>
                                    <small class="form-text text-muted">
                                        <i class="fa fa-info-circle"></i>
                                        Product is required for Jira synchronization
                                    </small>
                                </div>
                            </div>
                            
                            <div class="col-12 mb-3">
                                <div class="form-group">
                                    <label>Priority</label>
                                    <select class="form-control" v-model="ticket.priority">
                                        <option value="Low">Low</option>
                                        <option value="Medium" selected>Medium</option>
                                        <option value="High">High</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="col-12 mb-3">
                                <div class="form-group">
                                    <label>Description <span class="text-danger">*</span></label>
                                    <textarea class="form-control" 
                                              v-model="ticket.description" 
                                              rows="5" 
                                              required
                                              placeholder="Describe the issue or request in detail"></textarea>
                                </div>
                            </div>
                            
                            <div class="col-12 mb-3">
                                <div class="form-check">
                                    <input class="form-check-input" 
                                           type="checkbox" 
                                           v-model="autoSyncToJira" 
                                           id="autoSyncToJira">
                                    <label class="form-check-label" for="autoSyncToJira">
                                        Automatically sync to Jira after creation
                                    </label>
                                    <small class="form-text text-muted d-block">
                                        <i class="fa fa-info-circle"></i>
                                        Requires Jira integration to be configured
                                    </small>
                                </div>
                            </div>
                            
                            <div class="col-12">
                                <button type="submit" 
                                        class="btn btn-primary" 
                                        :disabled="isSubmitting">
                                    <i v-if="isSubmitting" class="fa fa-spinner fa-spin"></i>
                                    {{ isSubmitting ? 'Creating...' : 'Create Ticket' }}
                                </button>
                                <router-link :to="{ name: 'ticketList' }" 
                                             class="btn btn-secondary ms-2">Cancel</router-link>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Success Modal -->
    <div class="modal fade" id="successModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Ticket Created Successfully</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="alert alert-success">
                        <i class="fa fa-check-circle"></i>
                        <strong>Success!</strong> Your ticket has been created.
                        <br><br>
                        <strong>Ticket ID:</strong> {{ createdTicketId }}
                        <div v-if="jiraResult.success">
                            <br><strong>Jira Issue:</strong> {{ jiraResult.jira_issue_key }}
                        </div>
                        <div v-else-if="jiraResult.error">
                            <br><div class="alert alert-warning mt-2">
                                <strong>Jira Sync Failed:</strong> {{ jiraResult.error }}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <router-link :to="{ name: 'ticketList' }" class="btn btn-primary">View All Tickets</router-link>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AddTicket",
  data() {
    return {
      ticket: {
        title: "",
        description: "",
        customer_id: "",
        product_id: "",
        priority: "Medium"
      },
      customers: [],
      products: [],
      autoSyncToJira: false,
      isSubmitting: false,
      createdTicketId: null,
      jiraResult: {
        success: false,
        error: null,
        jira_issue_key: null
      }
    };
  },
  mounted() {
    this.axios = axios;
    this.loadCustomers();
    this.loadProducts();
  },
  methods: {
    async loadCustomers() {
      try {
        const response = await this.axios.get('http://localhost:5000/customers');
        this.customers = response.data;
      } catch (error) {
        console.error('Error loading customers:', error);
        alert('Failed to load customers');
      }
    },
    
    async loadProducts() {
      try {
        const response = await this.axios.get('http://localhost:5000/products');
        this.products = response.data;
      } catch (error) {
        console.error('Error loading products:', error);
        alert('Failed to load products');
      }
    },
    
    async submitTicket() {
      if (!this.validateForm()) {
        return;
      }
      
      this.isSubmitting = true;
      
      try {
        // Create the ticket
        const response = await this.axios.post('http://localhost:5000/tickets', this.ticket);
        this.createdTicketId = response.data.ticket_id;
        
        // If auto-sync is enabled and product is selected, sync to Jira
        if (this.autoSyncToJira && this.ticket.product_id) {
          await this.syncToJira(this.createdTicketId);
        }
        
        // Show success modal
        const modal = new bootstrap.Modal(document.getElementById('successModal'));
        modal.show();
        
      } catch (error) {
        console.error('Error creating ticket:', error);
        const errorMessage = error.response?.data?.message || 'Failed to create ticket';
        alert(errorMessage);
      } finally {
        this.isSubmitting = false;
      }
    },
    
    async syncToJira(ticketId) {
      try {
        const response = await this.axios.post(`http://localhost:5000/tickets/${ticketId}/sync-to-jira`);
        this.jiraResult = {
          success: true,
          jira_issue_key: response.data.jira_issue_key,
          error: null
        };
      } catch (error) {
        console.error('Error syncing to Jira:', error);
        this.jiraResult = {
          success: false,
          error: error.response?.data?.error || 'Unknown error occurred',
          jira_issue_key: null
        };
      }
    },
    
    validateForm() {
      if (!this.ticket.title.trim()) {
        alert('Please enter a ticket title');
        return false;
      }
      
      if (!this.ticket.description.trim()) {
        alert('Please enter a ticket description');
        return false;
      }
      
      if (!this.ticket.customer_id) {
        alert('Please select a customer');
        return false;
      }
      
      if (!this.ticket.product_id) {
        alert('Please select a product. This is required for Jira synchronization.');
        return false;
      }
      
      return true;
    }
  }
};
</script>

<style scoped>
.text-danger {
  color: #dc3545 !important;
}

.form-text {
  margin-top: 0.25rem;
}

.fa {
  margin-right: 5px;
}

.alert {
  margin-bottom: 0;
}

.card-header h4 {
  margin-bottom: 0;
}

.form-check-label {
  font-weight: normal;
}
</style>