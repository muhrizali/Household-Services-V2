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
                <table class="table table-lg">
                    <tbody>
                        <tr>
                            <td class="text-lg font-bold underline">ID:</td>
                            <td>{{ customer.id }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">NAME:</td>
                            <td>{{ customer.user.fullname }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">EMAIL:</td>
                            <td>{{ customer.user.email }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">STATUS:</td>
                            <td>
                                <span v-if="customer.status === 'ACTIVE'" class="badge badge-lg badge-success">{{ customer.status }}</span>
                                <span v-else class="badge badge-lg badge-error">{{ customer.status }}</span>
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">ADDRESS:</td>
                            <td>{{ customer.address }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">PIN CODE:</td>
                            <td>{{ customer.pincode }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">JOINED:</td>
                            <td>{{ customer.created }}</td>
                        </tr>
                    </tbody>
                </table>

                <!-- Customer Actions -->
                <div class="flex items-center justify-end gap-4">
                    <a href="">
                        <button class="btn btn-sm btn-success">Activate</button>
                    </a>
                    <a href="">
                        <button class="btn btn-sm btn-error">Block</button>
                    </a>
                </div>
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