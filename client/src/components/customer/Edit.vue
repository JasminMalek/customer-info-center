<template>
    <div class="row mt-1">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h4>Update Customer</h4>
                </div>
                <div class="card-body">
                    <form @submit.prevent="update">
                        <div class="row">
                            <div class="col-12 mb-2">
                                <div class="form-group">
                                    <label>Name</label>
                                    <input type="text" class="form-control" v-model="customer.name">
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
                                    <label>Email</label>
                                    <input type="text" class="form-control" v-model="customer.email">
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
                                    <input type="tel" class="form-control" v-model="customer.phone_number" @input="validatePhoneNumber">
<!--                                    <div v-if="!isPhoneNumberValid" class="text-danger">Invalid phone number.</div>                                -->
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
                                <button type="submit" class="btn btn-primary">Update</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
  name: "update-customer",
  data() {
    return {
      customer: {
        name: "",
        first_name: "",
        last_name: "",
        email: "",
        gender: "",
        phone_number: "",
        birthday: "",
        address: "",
        postcode: "",
        city: "",
        _method: "patch",
      },
    };
  },
  mounted() {
    this.axios = axios
    this.showCustomer();
  },
  methods: {
    async showCustomer() {
      await this.axios
        .get(`http://localhost:5000/customers/${this.$route.params.id}`)
        .then((response) => {
          const {
            name,
            first_name,
            last_name,
            email,
            gender,
            phone_number,
            birthday,
            address,
            postcode,
            city,
          } = response.data;
          this.customer.name = name;
          this.customer.first_name = first_name;
          this.customer.last_name = last_name;
          this.customer.email = email;
          this.customer.gender = gender;
          this.customer.phone_number = phone_number;
          this.customer.birthday = birthday;
          this.customer.address = address;
          this.customer.postcode = postcode;
          this.customer.city = city;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async update() {
      await this.axios
        .put(`http://localhost:5000/customers/${this.$route.params.id}`, this.customer)
        .then(() => {
          this.$router.push({ name: "customerList" });
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>

</style>
