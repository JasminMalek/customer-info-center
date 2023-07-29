<template>
    <div class="row mt-2">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h4>Customer Details</h4>
                </div>
                <div class="card-body">
                    <div class="form-group">
                        <label class="fw-bold">Name</label>
                        <p>{{ customer.name }}</p>
                    </div>
                    <div class="form-group">
                        <label class="fw-bold">First Name</label>
                        <p>{{ customer.first_name ?? '-' }}</p>
                    </div>
                    <div class="form-group">
                        <label class="fw-bold">Last Name</label>
                        <p>{{ customer.last_name ?? '-'}}</p>
                    </div>
                    <div class="form-group">
                        <label class="fw-bold">Email</label>
                        <p>{{ customer.email }}</p>
                    </div>
                    <div class="form-group">
                        <label class="fw-bold">Gender</label>
                        <p>{{ customer.gender_string ?? '-'}}</p>
                    </div>
                    <div class="form-group">
                        <label class="fw-bold">Phone Number</label>
                        <p>{{ customer.phone_number === '' ? 'No phone number added' : customer.phone_number }}</p>
                    </div>
                    <div class="form-group">
                        <label class="fw-bold">Birthday</label>
                        <p>{{ customer.birthday ?? '-'}}</p>
                    </div>
                    <div class="form-group">
                        <label class="fw-bold">Address</label>
                        <p>{{ customer.address ?? '-'}}</p>
                    </div>
                    <div class="form-group">
                        <label class="fw-bold">Postcode</label>
                        <p>{{ customer.postcode ?? '-'}}</p>
                    </div>
                    <div class="form-group">
                        <label class="fw-bold">City</label>
                        <p>{{ customer.city ?? '-'}}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CustomerShow",
    data() {
        return {
            customer: {},
        };
    },
    mounted() {
        this.axios = axios
        this.getCustomerData();
    },
    methods: {
        async getCustomerData() {
            const customerId = this.$route.params.id;
            try {
                const response = await this.axios.get(`http://localhost:5000/customers/${customerId}`);
                this.customer = response.data;
            } catch (error) {
                console.log(error);
            }
        },
    },
};
</script>
