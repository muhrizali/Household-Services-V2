<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getAPI } from '@/httpreqs';

const route = useRoute();
const serviceID = route.params.sid;

const serviceFound = ref(false);
const service = ref({});

const professionalsFound = ref(false);
const professionals = ref([]);

const message = ref("");

async function initialLoad() {
    const serviceResponse = await getAPI({ url: "/api/service", params: { "id": serviceID } });
    if (serviceResponse.data.found) {
        serviceFound.value = true;
        service.value = serviceResponse.data.service;
    } else {
        serviceFound.value = false;
    }

    const professionalsResponse = await getAPI({ url: '/api/professional', params: { 'sid': serviceID } });
    if (professionalsResponse.data.found) {
        professionalsFound.value = true;
        professionals.value = professionalsResponse.data.professionals;
    } else {
        professionalsFound.value = false;
    }
}

onMounted(initialLoad)

</script>
<template>
    <!-- Services Details -->
    <section class="w-2/3 card card-bordered border-2">
        <div class="card-body">
            <h2 class="card-title text-lg">SERVICE DETAILS:</h2>
            <div v-if="serviceFound">
                <table class="table table-sm">
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

    <!-- Professionals Offering the Service -->
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">PROFESSIONALS FOR {{ service.name }}</h2>
            <div v-if="professionalsFound">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>NAME</th>
                            <th>SERVICE</th>
                            <th>RATING</th>
                            <th>APPROVAL STATUS</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="prof in professionals">
                            <td>
                                <a href="{ url_for('customer_prof_details', cust_id=customer.id, prof_id=prof.id) }">
                                    <button class="btn btn-sm">{{ prof.id }}</button>
                                </a>
                            </td>
                            <td>{{ prof.user.fullname }}</td>
                            <td>{{ prof.service.name }}</td>
                            <td>{{ prof.avg_rating }}</td>
                            <td>
                                <span v-if="prof.approval === 'PENDING'" class="badge badge-lg border-dashed">{{ prof.approval }}</span>
                                <span v-else-if="prof.approval === 'REJECTED'" class="badge badge-lg badge-error">{{ prof.approval }}</span>
                                <span v-else class="badge badge-lg badge-success">{{ prof.approval }}</span>
                            </td>
                            <td>
                                <span>
                                    <a
                                        href="{ url_for('customer_service_book', cust_id=customer.id, service_id=service.id, prof_id=prof.id) }">
                                        <button class="btn btn-sm btn-success">Book</button>
                                    </a>
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                <p class="text-center font-bold text-error-content text-lg">No Professionals Found</p>
            </div>
        </div>
    </section>
</template>