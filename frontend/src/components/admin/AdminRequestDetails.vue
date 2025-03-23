<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getWithParamsAPI } from '@/httpreqs';
const route = useRoute();
const serviceRequestID = route.params.id;

const serviceRequest = ref({});
const serviceRequestFound = ref(false);
const message = ref("");

onMounted(async function () {
    try {
        const response = await getWithParamsAPI({ url: "/api/request", params: { "id": serviceRequestID } });
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
                            <td class="text-lg font-bold">ID:</td>
                            <td>{{ serviceRequest.id }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">CUSTOMER:</td>
                            <td>
                                {{ serviceRequest.customer.user.fullname }}
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">CONTACT:</td>
                            <td>
                                {{ serviceRequest.customer.contact }}
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">LOCATION:</td>
                            <td>
                                {{ serviceRequest.customer.address }}
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">PIN CODE:</td>
                            <td>
                                {{ serviceRequest.customer.pincode }}
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">SERVICE:</td>
                            <td>{{ serviceRequest.service.name }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">PROFESSIONAL:</td>
                            <td>
                                <span v-if="serviceRequest.status === 'REQUESTED'">NOT ASSIGNED</span>
                                <span v-else>{{ serviceRequest.professional?.user?.fullname }}</span>
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">STATUS:</td>
                            <td>
                                <span v-if="serviceRequest.status === 'REQUESTED'" class="badge badge-lg badge-error">REQUESTED</span>
                                <span v-else-if="serviceRequest.status === 'ASSIGNED'" class="badge badge-lg badge-warning">ASSIGNED</span>
                                <span v-else class="badge badge-lg badge-success">CLOSED</span>
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">RATING:</td>
                            <td>{{ serviceRequest.stars }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">REVIEW:</td>
                            <td>{{ serviceRequest.remarks }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">COMPLETED:</td>
                            <td>{{ serviceRequest.completed }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">CREATED:</td>
                            <td>{{ serviceRequest.created }}</td>
                        </tr>
                    </tbody>
                </table>

                <!-- Service Request Actions -->
                <div class="flex justify-end gap-2">
                    <RouterLink :to="{ name: 'admin_request_edit', params: { id: serviceRequest.id } }">
                        <button class="btn btn-sm btn-warning">✏️ EDIT</button>
                    </RouterLink>
                    <RouterLink :to="{ name: 'admin_request_delete', params: { id: serviceRequest.id } }">
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