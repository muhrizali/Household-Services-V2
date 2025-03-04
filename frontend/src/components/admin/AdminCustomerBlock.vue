<script setup>
import { putAPI, getAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();
const customerID = route.params.id;

const customerFound = ref(false);
const customer = ref({});

const message = ref("");

onMounted(async function () {
    try {
        const response = await getAPI({ url: "/api/customer", params: { "id": customerID } });
        if (response.data.found) {
            customerFound.value = true;
            customer.value = response.data.customer;
        }
    } catch {
        customerFound.value = false;
    }
});

async function onBlockClick() {
    try {
        const response = await putAPI({ url: "/api/customer", data: { "block_selected": true, "ids": [customerID] } });
        if (response.data.edited) {
            message.value = "Customer Blocked Successfully\nRedirecting back to home";
            setTimeout(() => router.push({ name: "admin_home" }), 2000);
        } else {
            message.value = "Customer Could Not be Blocked";
        }
    } catch {
        message.value = "Error While Blocking Customer";
    }
}

</script>
<template>
    <div class="card w-1/4 border-2 rounded-sm border-primary-content/25">
        <div class="card-body">
            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                <p class="text-center text-lg font-bold">{{ message }}</p>
            </div>

            <div v-if="customerFound">
                <h2 class="text-lg text-center font-semibold">
                    Do you want to block the customer {{ customer.user.fullname }}?
                </h2>
                <form class="form-control mt-4">
                    <div class="flex items-center justify-center gap-4">
                        <button @click.prevent="onBlockClick" class="btn btn-block btn-error">Block</button>
                    </div>
                </form>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested Customer Not Found</p>
            </div>

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'admin_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </div>
</template>