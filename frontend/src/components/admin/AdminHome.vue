<script setup>
import AdminServicesSection from './AdminServicesSection.vue';
import AdminProfessionalSection from './AdminProfessionalSection.vue';
import AdminCustomerSection from './AdminCustomerSection.vue';
import AdminRequestSection from './AdminRequestSection.vue';
</script>
<template>
    <!-- SERVICES SECTION -->
    <AdminServicesSection :items="[]" />
    <!-- PROFESSIONALS SECTION -->
    <AdminProfessionalSection :items="[]" />
    <!-- CUSTOMERS SECTION -->
    <AdminCustomerSection :items="[]" />
    <!-- REQUESTS SECTION -->
    <AdminRequestSection :items="[]" />
</template>