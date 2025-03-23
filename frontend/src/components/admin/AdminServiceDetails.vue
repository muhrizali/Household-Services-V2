<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getWithParamsAPI } from '@/httpreqs';
const route = useRoute();
const serviceID = route.params.id;

const serviceFound = ref(false);
const service = ref({});
const message = ref("");

onMounted(async function () {
    try {
        const response = await getWithParamsAPI({ url: "/api/service", params: { "id": serviceID } });
        if (response.data.found) {
            serviceFound.value = true;
            service.value = response.data.service;
        } else {
            serviceFound.value = false;
        }
    } catch (error) {
        message.value = "Something Went Wrong";
    }
})

</script>
<template>
    <!-- Services Details -->
    <section class="w-2/3 card card-bordered border-2">
        <div class="card-body">
            <h2 class="card-title text-lg">Service Details:</h2>
            <div v-if="serviceFound">
                <table class="table table-sm">
                    <tbody>
                        <tr>
                            <td class="text-lg font-bold">ID:</td>
                            <td>{{ service.id }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">NAME:</td>
                            <td>{{ service.name }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">DESCRIPTION:</td>
                            <td>{{ service.description }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">TIME REQUIRED:</td>
                            <td>{{ service.timereq }} Hours</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">PRICE:</td>
                            <td>{{ service.price }} Rupees</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">CREATED:</td>
                            <td>{{ service.created }}</td>
                        </tr>
                    </tbody>
                </table>
    
                <!-- Service Actions -->
                <div class="flex items-center justify-end gap-2">
                    <RouterLink :to="{ name: 'admin_service_edit', params: { id: service.id } }">
                        <button class="btn btn-sm btn-warning">✏️ EDIT</button>
                    </RouterLink>
                    <RouterLink :to="{ name: 'admin_service_delete', params: { id: service.id } }">
                        <button class="btn btn-sm btn-error">🗑️ DELETE</button>
                    </RouterLink>
                </div>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested Service Not Found</p>
            </div>
            <p class="text-center text-lg font-bold">{{ message }}</p>


            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'admin_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </section>
</template>