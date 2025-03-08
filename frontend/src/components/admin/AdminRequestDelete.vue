<script setup>
import { deleteAPI, getAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();
const serviceRequestID = route.params.id;

const serviceRequestFound = ref(false);
const serviceRequest = ref({});

const message = ref("");

onMounted(async function () {
    try {
        const response = await getAPI({ url: "/api/request", params: { id: serviceRequestID } });
        if (response.data.found) {
            serviceRequestFound.value = true;
            serviceRequest.value = response.data.service_request;
        }
    } catch {
        serviceRequestFound.value = false;
    }
});

async function onDeleteClick() {
    try {
        const response = await deleteAPI({ url: "/api/request", params: { "id": serviceRequestID } });
        if (response.data.deleted) {
            message.value = "Service Request Deleted Successfully\nRedirecting back to home";
            setTimeout(() => router.push({ name: "admin_home" }), 2000);
        } else {
            message.value = "Service Request Could Not be Deleted";
        }
    } catch {
        message.value = "Error While Deleting Service Request";
    }
}

</script>
<template>
    <div class="card w-1/4 border-2 rounded-sm border-primary-content/25">
        <div class="card-body">
            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                <p class="text-center text-lg font-bold">{{ message }}</p>
            </div>

            <div v-if="serviceRequestFound">
                <h2 class="text-lg text-center font-semibold">
                    Do you want to delete the service request with ID {{ serviceRequestID }}?
                </h2>
                <form class="form-control mt-4">
                    <div class="flex items-center justify-center gap-4">
                        <button @click.prevent="onDeleteClick" class="btn btn-block btn-error">DELETE</button>
                    </div>
                </form>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested Service Request Not Found</p>
            </div>

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'admin_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </div>
</template>