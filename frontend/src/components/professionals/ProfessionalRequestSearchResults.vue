<script setup>
import { getAPI } from '@/httpreqs';
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps(['items']);

const route = useRoute();
const professionalID = route.params.id;

const serviceRequestsFound = ref(false);
const serviceRequests = ref([]);
const message = ref('');

async function initialLoad() {
    const response = await getAPI({ url: '/api/request', params: { 'pid': professionalID, 'new_requests': true } });
    if (response.data.found) {
        serviceRequestsFound.value = true;
        serviceRequests.value = response.data.requests;
    } else {
        message.value = 'No New Requests Yet';
    }
}


watch(() => props.items, (newItems, oldItems) => {
    serviceRequests.value = newItems;
});


onMounted(async function () {
    if (props.items?.length) {
        serviceRequests.value = props.items;
        serviceRequestsFound.value = true;
    } else {
        initialLoad();
    }
});

</script>
<template>
    <!-- Accepted Resquests List Table -->
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">NEW REQUESTS</h2>
            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                <p class="text-center text-lg font-bold">{{ message }}</p>
            </div>
            <div v-if="serviceRequestsFound">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>CUSTOMER</th>
                            <th>CREATED</th>
                            <th>LOCATION</th>
                            <th>STATUS</th>
                            <th>PIN CODE</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="serviceRequest in serviceRequests">
                            <td>
                                <RouterLink
                                    :to="{ name: 'professional_request_details', params: { 'rid': serviceRequest.id } }"
                                    class="btn btn-sm">{{ serviceRequest.id }}</RouterLink>

                            </td>
                            <td>{{ serviceRequest.customer.user.fullname }}</td>
                            <td>{{ serviceRequest.created }}</td>
                            <td>{{ serviceRequest.customer.address }}</td>
                            <td>
                                <span v-if="serviceRequest.status === 'REQUESTED'"
                                    class="badge badge-lg badge-error">REQUESTED</span>
                                <span v-else-if="serviceRequest.status === 'ASSIGNED'"
                                    class="badge badge-lg badge-warning">ASSIGNED</span>
                                <span v-else class="badge badge-lg badge-success">CLOSED</span>
                            </td>
                            <td>{{ serviceRequest.customer.pincode }}</td>
                            <td>
                                <span>
                                    <RouterLink v-if="serviceRequest.status === 'REQUESTED'"
                                        :to="{ name: 'professional_request_accept', params: { 'rid': serviceRequest.id } }">
                                        <button class="btn btn-sm btn-success">ACCEPT</button>
                                    </RouterLink>
                                    <RouterLink v-if="serviceRequest.status === 'ASSIGNED'"
                                        :to="{ name: 'professional_request_reject', params: { 'rid': serviceRequest.id } }">
                                        <button class="btn btn-sm btn-error">REJECT</button>
                                    </RouterLink>
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>
</template>