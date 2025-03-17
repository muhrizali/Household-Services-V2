<script setup>
import { putAPI, getAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();
const professionalID = route.params.id;
const serviceRequestID = route.params.rid;

const serviceRequestFound = ref(false);
const serviceRequest = ref({});

const message = ref("");

function serviceRequestRejectData() {
    return {
        'id': serviceRequestID,
        'pid': professionalID,
        'reject_request': true,
    }
}

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

async function onRejectClick() {
    try {
        const response = await putAPI({ url: "/api/request", data: serviceRequestRejectData() });
        if (response.data.edited) {
            message.value = "Service Request Rejected Successfully\nRedirecting back to home";
            setTimeout(() => router.push({ name: "professional_home" }), 2000);
        } else {
            message.value = "Service Request Could Not be Reject";
        }
    } catch {
        message.value = "Error While Rejecting Service Request";
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
                    Do you want to reject the service request with ID {{ serviceRequestID }}?
                </h2>
                <form class="form-control mt-4">
                    <div class="flex items-center justify-center gap-4">
                        <button @click.prevent="onRejectClick" class="btn btn-block btn-error">REJECT</button>
                    </div>
                </form>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested Service Request Not Found</p>
            </div>

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'professional_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </div>
</template>