<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getWithParamsAPI } from '@/httpreqs';
const route = useRoute();
const customerID = route.params.id;

const customer = ref({});
const customerFound = ref(false);
const message = ref("");

onMounted(async function () {
    try {
        const response = await getWithParamsAPI({ url: "api/customer", params: { "id": customerID } });
        if (response.data.found) {
            customerFound.value = true;
            customer.value = response.data.customer;
        } else {
            customerFound.value = false;
        }
    } catch (error) {
        message.value = "Something Went Wrong";
    }
})

</script>
<template>
    <section class="w-2/3 card card-bordered border-2">
        <div class="card-body">
            <div v-if="customerFound">
                <h2 class="card-title text-lg">CUSTOMER DETAILS:</h2>
                <table class="table table-sm">
                    <tbody>
                        <tr>
                            <td class="text-lg font-bold ">ID:</td>
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
                            <td class="text-lg font-bold">STATUS:</td>
                            <td>
                                <span v-if="customer.status === 'ACTIVE'" class="badge badge-lg badge-success">{{ customer.status }}</span>
                                <span v-else class="badge badge-lg badge-error">{{ customer.status }}</span>
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
                <span class="flex justify-end gap-2">
                    <RouterLink :to="{ name: 'admin_customer_activate', params: { id: customer.id } }">
                        <button class="btn btn-sm btn-success">✅ ACTIVATE</button>
                    </RouterLink>
                    <RouterLink :to="{ name: 'admin_customer_block', params: { id: customer.id } }">
                        <button class="btn btn-sm btn-error">❌ BLOCK</button>
                    </RouterLink>
                </span>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested Customer Not Found</p>
            </div>
            <p class="text-center text-lg font-bold">{{ message }}</p>

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'admin_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </section>
</template>