<script setup>
import { deleteWithParamsAPI, getWithParamsAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();
const serviceID = route.params.id;

const serviceFound = ref(false);
const service = ref({});

const message = ref("");

onMounted(async function () {
    try {
        const response = await getWithParamsAPI({ url: "api/service", params: { "id": serviceID } });
        if (response.data.found) {
            serviceFound.value = true;
            service.value = response.data.service;
        }
    } catch {
        serviceFound.value = false;
    }
});

async function onDeleteClick() {
    try {
        const response = await deleteWithParamsAPI({ url: "api/service", params: { "id": serviceID } });
        if (response.data.deleted) {
            message.value = "Service Deleted Successfully\nRedirecting back to home";
            setTimeout(() => router.push({ name: "admin_home" }), 2000);
        } else {
            message.value = "Service Could Not be Deleted";
        }
    } catch {
        message.value = "Error While Deleting Service";
    }
}

</script>
<template>
    <div class="card w-1/4 border-2 rounded-sm border-primary-content/25">
        <div class="card-body">
            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                <p class="text-center text-lg font-bold">{{ message }}</p>
            </div>

            <div v-if="serviceFound">
                <h2 class="text-lg text-center font-semibold">
                    Do you want to delete the service {{ service.name }}?
                </h2>
                <form class="form-control mt-4">
                    <div class="flex items-center justify-center gap-4">
                        <!-- {{ form.delete(class="btn btn-block btn-error", value="Delete") }} -->
                        <button @click.prevent="onDeleteClick" class="btn btn-block btn-error">DELETE</button>
                    </div>
                </form>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested Service Not Found</p>
            </div>

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'admin_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </div>
</template>