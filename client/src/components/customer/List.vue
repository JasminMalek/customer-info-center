<template>
  <div class="row">
    <div class="col-12 mt-2 mb-2 text-end">
      <router-link :to="{ name: 'customerAdd' }" class="btn btn-primary">Add New Customer</router-link>
    </div>
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <h4>Customer</h4>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone Number</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <template v-if="!loading">
                <tbody v-if="customers.length > 0">
                  <tr v-for="(customer, key) in customers" :key="key">
                    <td>{{ customer.id }}</td>
                    <td>{{ customer.name }}</td>
                    <td>{{ customer.email }}</td>
                    <td>{{ customer.phone_number === '' ? 'No phone number added' : customer.phone_number }}</td>
                    <td>
                      <router-link :to="{ name: 'customerEdit', params: { id: customer.id } }" class="btn btn-success" style="margin-right: 5px;">Edit</router-link>
                      <router-link :to="{ name: 'customerShow', params: { id: customer.id } }" class="btn btn-primary" style="margin-right: 5px;">View Details</router-link>
                      <button type="button" @click="deleteCustomer(customer.id)" class="btn btn-danger">Delete</button>
                    </td>
                  </tr>
                </tbody>
                <tbody v-else>
                  <tr>
                    <td colspan="5" align="center">No Customers Found.</td>
                  </tr>
                </tbody>
              </template>
              <tbody v-else>
                <tr>
                  <td colspan="5" class="text-center">
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
</template>

<script>
import axios from "axios";

export default {
  name: "CustomerList",
  data() {
    return {
      customers: [],
      loading: true,
    };
  },
  mounted() {
    this.axios = axios;
    this.getCustomers();
  },
  methods: {
    async getCustomers() {
      try {
        const response = await this.axios.get('http://localhost:5000/customers');
        this.customers = response.data; // The response should contain the array directly
      } catch (error) {
        console.error(error);
        this.customers = [];
      } finally {
        this.loading = false;
      }
    },
    async deleteCustomer(id) {
      const confirmed = window.confirm("Are you sure to delete this customer?");
      if (confirmed) {
        try {
          await this.axios.delete(`http://localhost:5000/customers/${id}`);
          alert('Customer deleted successfully'); // Show simple success alert
          await this.getCustomers(); // Refresh the customer list
        } catch (error) {
          console.error(error);
          alert('Failed to delete customer'); // Show error alert
        }
      }
    },
  },
};
</script>

<style scoped>
/* Your style code remains unchanged */
</style>
