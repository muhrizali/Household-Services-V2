<script setup>
import { getAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();

const customerID = route.params.id;

const customerFound = ref(false);
const customer = ref({});

const message = ref('');

async function initialLoad() {
  const response = await getAPI({ url: '/api/customer', params: { 'id': customerID } });
  if (response.data.found) {
    customerFound.value = true;
    customer.value = response.data.customer;
  } else {
    message.value = 'Customer Not Found';
  }
}

onMounted(initialLoad);

</script>
<template>
    <section class="w-2/3 card card-bordered border-2">
        <div class="card-body">
            <div v-if="customerFound">
                <h2 class="card-title text-lg">CUSTOMER DETAILS:</h2>
                <table class="table table-sm">
                    <tbody>
                        <tr>
                            <td class="text-lg font-bold">ID:</td>
                            <td>{{ customer.id }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">NAME:</td>
                            <td>{{ customer.user.fullname }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">EMAIL:</td>
                            <td>{{ customer.user.email }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">CONTACT:</td>
                            <td>{{ customer.contact }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">STATUS:</td>
                            <td>
                                <span v-if="customer.status === 'BLOCKED'" class="badge badge-lg badge-error">{{
                                    customer.status }}</span>
                                <span v-else-if="customer.status === 'ACTIVE'" class="badge badge-lg badge-success">{{
                                    customer.status }}</span>
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">ADDRESS:</td>
                            <td>{{ customer.address }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">PIN CODE:</td>
                            <td>{{ customer.pincode }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">JOINED:</td>
                            <td>{{ customer.created }}</td>
                        </tr>
                    </tbody>
                </table>
                <!-- Customer Actions -->
                <div class="flex items-center justify-end gap-2">
                    <RouterLink :to="{ name: 'customer_profile_edit' }">
                        <button class="btn btn-sm btn-primary">EDIT</button>
                    </RouterLink>
                </div>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested customer not found</p>
            </div>

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'customer_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </section>
</template>