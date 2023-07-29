<template>
  <div className="container">
    <nav className="navbar navbar-expand-lg navbar-light bg-light" style="background-color: #E6E6FA;">
      <div className="collapse navbar-collapse">
        <div className="navbar-nav">
          <router-link to="/customer" className="nav-item nav-link">Customers List</router-link>
          <router-link to="/customer/add" className="nav-item nav-link">Create New Customer</router-link>
        </div>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css';
export default {}
</script>
