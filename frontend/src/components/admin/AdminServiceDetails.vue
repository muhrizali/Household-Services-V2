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
        const response = await getWithParamsAPI({ url: "api/service", params: { "id": serviceID } });
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
                <table class="table table-lg">
                    <tbody>
                        <tr>
                            <td class="text-lg font-bold underline">ID:</td>
                            <td>{{ service.id }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">NAME:</td>
                            <td>{{ service.name }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">DESCRIPTION:</td>
                            <td>{{ service.description }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">TIME REQUIRED (Approx.):</td>
                            <td>{{ service.timereq }} Hours</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">PRICE:</td>
                            <td>{{ service.price }} Rupees</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">CREATED:</td>
                            <td>{{ service.created }}</td>
                        </tr>
                    </tbody>
                </table>
    
                <!-- Service Actions -->
                <div class="flex items-center justify-end gap-2">
                    <a href="">
                        <button class="btn btn-sm btn-warning">Edit</button>
                    </a>
                    <a href="">
                        <button class="btn btn-sm btn-error">Delete</button>
                    </a>
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