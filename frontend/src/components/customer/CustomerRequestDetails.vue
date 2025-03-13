<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getAPI } from '@/httpreqs';
const route = useRoute();
const serviceRequestID = route.params.rid;

const serviceRequest = ref({});
const serviceRequestFound = ref(false);
const message = ref("");

onMounted(async function () {
    try {
        const response = await getAPI({ url: "/api/request", params: { "id": serviceRequestID } });
        if (response.data.found) {
            serviceRequestFound.value = true;
            serviceRequest.value = response.data.service_request;
        } else {
            serviceRequestFound.value = false;
        }
    } catch (error) {
        message.value = "Something Went Wrong";
    }
})

</script>
<template>
    <section class="w-2/3 card card-bordered border-2">
        <div class="card-body">
            <div v-if="serviceRequestFound">
                <h2 class="card-title text-lg">SERVICE REQUEST DETAILS:</h2>
                <table class="table table-sm">
                    <tbody>
                        <tr>
                            <td class="text-lg font-bold underline">ID:</td>
                            <td>{{ serviceRequest.id }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">CUSTOMER:</td>
                            <td>
                                {{ serviceRequest.customer.user.fullname }}
                                <!-- <a href="#" class="link link-primary"></a> -->
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">SERVICE:</td>
                            <td>{{ serviceRequest.service.name }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">PROFESSIONAL:</td>
                            <td>
                                <span v-if="serviceRequest.status === 'REQUESTED'">NOT ASSIGNED</span>
                                <span v-else>{{ serviceRequest.professional?.user?.fullname }}</span>
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">STATUS:</td>
                            <td>
                                <span v-if="serviceRequest.status === 'REQUESTED'" class="badge badge-lg badge-error">REQUESTED</span>
                                <span v-else-if="serviceRequest.status === 'ASSIGNED'" class="badge badge-lg badge-warning">ASSIGNED</span>
                                <span v-else class="badge badge-lg badge-success">CLOSED</span>
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">RATING:</td>
                            <td>{{ serviceRequest.stars }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">REVIEW:</td>
                            <td>{{ serviceRequest.remarks }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">COMPLETED:</td>
                            <td>{{ serviceRequest.completed }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">CREATED:</td>
                            <td>{{ serviceRequest.created }}</td>
                        </tr>
                    </tbody>
                </table>

                <!-- Service Request Actions -->
                <div class="flex justify-end gap-2">
                    <RouterLink v-if="serviceRequest.status === 'REQUESTED'" :to="{}">
                        <button class="btn btn-sm btn-error">❌ CANCEL</button>
                    </RouterLink>
                    <RouterLink v-if="serviceRequest.status === 'ASSIGNED'" :to="{}">
                        <button class="btn btn-sm btn-primary">🗑️ CLOSE?</button>
                    </RouterLink>
                </div>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested Service Not Found</p>
            </div>
            <p class="text-center text-lg font-bold">{{ message }}</p>

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'customer_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </section>
</template>