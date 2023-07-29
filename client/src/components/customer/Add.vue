<template>
    <div class="row mt-2">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h4>Add Customer</h4>
                </div>
                <div class="card-body">
                    <form @submit.prevent="create">
                        <div class="row">
                            <div class="col-12 mb-2">
                                <div class="form-group">
                                    <label class="required-label">Name</label>
                                    <input type="text" class="form-control" v-model="customer.name" required>
                                </div>
                            </div>
                            <div class="col-6 mb-2">
                                <div class="form-group">
                                    <label>First Name</label>
                                    <input type="text" class="form-control" v-model="customer.first_name">
                                </div>
                            </div>
                            <div class="col-6 mb-2">
                                <div class="form-group">
                                    <label>Last Name</label>
                                    <input type="text" class="form-control" v-model="customer.last_name">
                                </div>
                            </div>
                            <div class="col-12 mb-2">
                                <div class="form-group">
                                    <label class="required-label">Email</label>
                                    <input type="email" class="form-control" v-model="customer.email" required>
                                </div>
                            </div>
                            <div class="col-12 mb-2">
                                <div class="form-group">
                                    <label>Gender</label>
                                    <select class="form-control" v-model="customer.gender">
                                        <option value="1">Female</option>
                                        <option value="2">Male</option>
                                        <option value="0">Unspecified</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-12 mb-2">
                                <div class="form-group">
                                    <label>Phone Number</label>
                                    <input type="tel" class="form-control" v-model="customer.phone_number">
                                </div>
                            </div>
                            <div class="col-12 mb-2">
                                <div class="form-group">
                                    <label>Birthday</label>
                                    <input type="date" class="form-control" v-model="customer.birthday">
                                </div>
                            </div>
                            <div class="col-12 mb-2">
                                <div class="form-group">
                                    <label>Address</label>
                                    <textarea class="form-control" v-model="customer.address" rows="3"></textarea>
                                </div>
                            </div>
                            <div class="col-12 mb-2">
                                <div class="form-group">
                                    <label>Postcode</label>
                                    <input type="text" class="form-control" v-model="customer.postcode">
                                </div>
                            </div>
                            <div class="col-12 mb-2">
                                <div class="form-group">
                                    <label>City</label>
                                    <input type="text" class="form-control" v-model="customer.city">
                                </div>
                            </div>
                            <div class="col-12">
                                <button type="submit" class="btn btn-primary">Save</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name:"AddCustomer",
    data(){
        return {
            customer: {
              name: '',
              email: ''
            }
        }
    },
   methods: {
      async create() {
        try {
          await axios.post('http://localhost:5000/customers', this.customer)
          this.$router.push({name: "customerList"});
        } catch (error) {
          console.log(error);
        }
      }
   }
}
</script>

<style scoped>
.required-label::after {
    content: "*";
    color: red;
}
</style>
