<script setup>
import { onMounted, ref } from 'vue';
import { getAPI } from '@/httpreqs';
const requests = ref([]);

onMounted(async function () {
    const response = await getAPI({ url: "/api/request" });
    requests.value = response.data.requests;
});
</script>
<template>
    <!-- Service Requests List Table -->
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">SERVICE REQUESTS</h2>
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>CUSTOMER</th>
                        <th>SERVICE</th>
                        <th>PROFESSIONAL</th>
                        <th>REQUESTED</th>
                        <th>STATUS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="requests.length" v-for="request in requests">
                        <td>
                            <RouterLink :to="{ name: 'admin_request_details', params: { id: request.id } }">
                                <button class="btn btn-sm">{{ request.id }}</button>
                            </RouterLink>
                        </td>
                        <td>{{ request.customer.user.fullname }}</td>
                        <td>{{ request.service.name }}</td>
                        <td>
                            <span v-if="request.status === 'REQUESTED'">NOT ASSIGNED</span>
                            <span v-else>{{ request.professional.user.fullname }}</span>
                        </td>
                        <td>{{ request.created }}</td>
                        <td>
                            <span v-if="request.status === 'REQUESTED'"
                                class="badge badge-lg badge-error">REQUESTED</span>
                            <span v-else-if="request.status === 'ASSIGNED'"
                                class="badge badge-lg badge-warning">ASSIGNED</span>
                            <span v-else class="badge badge-lg badge-success">CLOSED</span>
                        </td>
                        <td>
                            <span class="flex gap-2">
                                <RouterLink :to="{ name: 'admin_request_edit', params: { id: request.id } }">
                                    <button class="btn btn-sm btn-warning">EDIT</button>
                                </RouterLink>
                                <a href="">
                                    <button class="btn btn-sm btn-error">DELETE</button>
                                </a>
                            </span>
                        </td>
                    </tr>
                    <tr v-else>
                        <td colspan="6" class="text-center font-bold text-error-content text-lg">No Requests Found</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
</template>