<script setup>
import { onMounted, ref } from 'vue';
import { getAPI } from '@/httpreqs';
const customers = ref([]);

onMounted(async function () {
    const response = await getAPI({ url: "/api/customer" });
    customers.value = response.data.customers;
})
</script>
<template>
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">CUSTOMERS</h2>
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>NAME</th>
                        <th>EMAIL</th>
                        <th>CONTACT</th>
                        <th>STATUS</th>
                        <th>JOINED</th>
                        <th>ACTIONS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="customers.length" v-for="customer in customers">
                        <td>
                            <RouterLink :to="{ name: 'admin_customer_details', params: { id: customer.id } }" class="btn btn-sm">{{ customer.id }}</RouterLink>
                        </td>
                        <td>{{ customer.user.fullname }}</td>
                        <td>{{ customer.user.email }}</td>
                        <td>{{ customer.contact }}</td>
                        <td>
                            <span v-if="customer.status === 'ACTIVE'" class="badge badge-lg badge-success">{{ customer.status }}</span>
                            <span v-else class="badge badge-lg badge-error">{{ customer.status }}</span>
                        </td>
                        <td>{{ customer.created }}</td>
                        <td>
                            <span class="flex gap-2">
                                <RouterLink :to="{ name: 'admin_customer_activate', params: { id: customer.id } }">
                                    <button class="btn btn-sm btn-success">ACTIVATE</button>
                                </RouterLink>
                                <RouterLink :to="{ name: 'admin_customer_block', params: { id: customer.id } }">
                                    <button class="btn btn-sm btn-error">BLOCK</button>
                                </RouterLink>
                            </span>
                        </td>
                    </tr>
                    <tr v-else>
                        <td colspan="7" class="text-center font-bold text-error-content text-lg">No Customers Found</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
</template>