<script setup>
import { getAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';

const servicesFound = ref(false);
const services = ref([]);
const message = ref('');

async function initialLoad() {
    const response = await getAPI({ url: '/api/service' });
    if (response.data.found) {
        servicesFound.value = true;
        services.value = response.data.services;
    } else {
        message.value = 'Services not found';
    }
}

onMounted(initialLoad);

</script>
<template>
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">SERVICE SHOWCASE:</h2>
            <div v-if="servicesFound">
                <div class="grid grid-rows-3 grid-flow-col auto-cols-[32.15%] overflow-x-auto gap-4 p-4 h-56">
                    <!-- TODO: SERVICE FLEX -->
                    <!-- Item -->
                    <RouterLink v-for="service in services"
                        :to="{ name: 'customer_service_details', params: { sid: service.id } }"
                        class="pt-2 pl-2 rounded-md border-2 hover:bg-slate-200 hover:border-slate-400">
                        <div>
                            <h3 class="card-title font-medium text-lg text-base-content/75 hover:underline">{{ service.name }}</h3>
                        </div>
                    </RouterLink>
                </div>
            </div>
            <div v-else>
                <p class="text-xl text-center font-medium">Services not found</p>
            </div>
        </div>
    </section>
</template>