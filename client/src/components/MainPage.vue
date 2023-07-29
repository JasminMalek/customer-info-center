<template>
    <div class="welcome-container">
        <div class="welcome-content">
            <h1 class="welcome-title">Customer Info Hub</h1>
            <p class="welcome-description">Welcome to our customer information hub. Manage your customer data efficiently.</p>
            <router-link :to="{ name: 'customerList' }" class="btn btn-outline-primary">Get Started</router-link>
        </div>
    </div>
</template>

<script>
export default {};
</script>

<style scoped>
.welcome-container {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

.welcome-content {
    text-align: center;
}

.welcome-title {
    font-size: 3rem;
    margin-bottom: 20px;
    color: #333333;
}

.welcome-description {
    font-size: 1.2rem;
    color: #474747;
    margin-bottom: 30px;
}
</style>
