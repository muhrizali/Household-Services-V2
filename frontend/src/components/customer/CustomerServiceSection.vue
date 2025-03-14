<script setup>
import { onMounted, ref, watch } from 'vue';
import { getAPI } from '@/httpreqs';

const props = defineProps(['items']);

const services = ref([]);

const message = ref("");

async function initialLoad() {
    const response = await getAPI({ url: "/api/service", params: { all: true } });
    services.value = response.data.services;
}


watch(() => props.items, (newItems, oldItems) => {
    services.value = newItems;
})

onMounted(async function () {
    if (props.items?.length) {
        services.value = props.items;
    } else {
        initialLoad();
    }
})

</script>

<template>
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">SERVICES</h2>

            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                {{ message }}
            </div>

            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>SERVICE</th>
                        <th>PRICE</th>
                        <th>CREATED</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="services.length" v-for="service in services" :key="service.id">
                        <td>
                            <RouterLink :to="{ name: 'customer_service_details', params: { 'sid': service.id } }">
                                <button class="btn btn-sm">{{ service.id }}</button>
                            </RouterLink>
                        </td>
                        <td>{{ service.name }}</td>
                        <td>{{ service.price }}</td>
                        <td>{{ service.created }}</td>
                    </tr>
                    <tr v-else>
                        <td colspan="4" class="text-center font-bold text-error-content text-lg">No Services Found</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
</template>