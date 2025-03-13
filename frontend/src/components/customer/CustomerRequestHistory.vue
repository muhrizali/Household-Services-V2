<script setup>
import { getAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const customerID = route.params.id;

const serviceRequestsFound = ref(false);
const serviceRequests = ref([]);
const message = ref('');

async function initialLoad() {
    const response = await getAPI({ url: '/api/request', params: { cid: customerID } });
    if (response.data.found) {
        serviceRequestsFound.value = true;
        serviceRequests.value = response.data.requests;
    } else {
        message.value = 'Service Request Not Found';
    }
}

onMounted(initialLoad);

</script>
<template>
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">SERVICE REQUEST HISTORY:</h2>
            <div v-if="serviceRequestsFound">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>SERVICE</th>
                        <th>PROFESSIONAL</th>
                        <th>CONTACT</th>
                        <th>REQUESTED</th>
                        <th>STATUS</th>
                        <th>ACTIONS</th>
                    </tr>
                </thead>
                    <tbody>
                        <tr v-for="serviceRequest in serviceRequests">
                            <td>
                                <RouterLink :to="{ name: 'customer_request_details', params: { rid: serviceRequest.id } }"
                                    class="btn btn-sm">
                                    {{ serviceRequest.id }}
                                </RouterLink>
                            </td>
                            <td>{{ serviceRequest.service.name }}</td>
                            <td>
                                <span v-if="serviceRequest.status === 'REQUESTED'">NOT ASSIGNED</span>
                                <span v-else>{{ serviceRequest.professional.user.fullname }}</span>
                            </td>
                            <td>
                                <span v-if="serviceRequest.status === 'REQUESTED'">NONE</span>
                                <span v-else>{{ serviceRequest.professional.contact }}</span>
                            </td>
                            <td>{{ serviceRequest.created }}</td>
                            <!-- Status of request: -->
                            <!-- can be "Close?", "Closed", "Requested" -->
                            <td>
                                <span v-if="serviceRequest.status === 'REQUESTED'" class="badge badge-lg badge-error">{{ serviceRequest.status }}</span>
                                <span v-else-if="serviceRequest.status === 'CLOSED'" class="badge badge-lg badge-success">{{ serviceRequest.status }}</span>
                                <span v-else class="badge badge-lg badge-warning">{{ serviceRequest.status }}</span>
                            </td>
                            <td>
                                <RouterLink
                                    v-if="serviceRequest.status === 'REQUESTED'"
                                    :to="{ name: 'customer_request_cancel', params: { rid: serviceRequest.id } }">
                                    <span class="btn btn-sm btn-error">CANCEL</span>
                                </RouterLink>
                                <a  
                                    v-if="serviceRequest.status === 'ASSIGNED'"
                                    href="{ url_for('customer_request_close', cust_id=customer.id, req_id=service_request.id) }">
                                    <span class="btn btn-sm btn-primary">CLOSE?</span>
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                <p class="text-xl text-center font-medium">Service Requests History not found</p>
            </div>
        </div>
    </section>
</template>