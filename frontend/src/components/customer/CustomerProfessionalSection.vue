<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref, watch } from 'vue';
import { getAPI } from '@/httpreqs';

const props = defineProps(['items']);

const route = useRoute();
const serviceID = route.params.sid;

const professionalsFound = ref(false);
const professionals = ref([]);

const message = ref("");

async function initialLoad() {
    const professionalsResponse = await getAPI({ url: '/api/professional', params: { 'sid': serviceID } });
    if (professionalsResponse.data.found) {
        professionalsFound.value = true;
        professionals.value = professionalsResponse.data.professionals;
    } else {
        professionalsFound.value = false;
    }
}

watch(() => props.items, (newItems, oldItems) => {
    professionals.value = newItems;
})


onMounted(async function () {
    if (props.items?.length) {
        professionalsFound.value = true;
        professionals.value = props.items;
    } else {
        initialLoad();
    }
});

</script>
<template>
    <!-- Professionals Offering the Service -->
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">PROFESSIONALS</h2>
            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                <p class="text-center text-lg font-bold">{{ message }}</p>
            </div>
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
                                <RouterLink :to="{ name: 'customer_professional_details', params: { sid: prof.service.id, pid: prof.id } }">
                                    <button class="btn btn-sm">{{ prof.id }}</button>
                                </RouterLink>
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
                                    <RouterLink
                                        :to="{ name: 'customer_request_book', params: { sid: prof.service.id, pid: prof.id } }">
                                        <button class="btn btn-sm btn-success">Book</button>
                                    </RouterLink>
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