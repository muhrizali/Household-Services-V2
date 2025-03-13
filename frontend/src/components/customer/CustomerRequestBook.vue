<script setup>
import { getAPI, postAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();

const customerID = route.params.id;
const serviceID = route.params.sid;
const professionalID = route.params.pid;

const message = ref('');

async function onBookClick() {
    const response = await postAPI({ url: "/api/request", data: { 'cid': customerID, 'sid': serviceID, 'pid': professionalID } });
    if (response.data.added) {
        message.value = 'Service Request Added Successfully';
        setTimeout(() => router.push({ name: 'customer_home' }), 2000)
    } else {
        message.value = 'Service Request could not be added';
    }
}

</script>
<template>
    <div class="card w-1/4 border-2 rounded-sm border-primary-content/25">
        <div class="card-body">
            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                <p class="text-center text-lg font-bold">{{ message }}</p>
            </div>

                <h2 class="text-lg text-center font-semibold">
                    Do you want to book the service with ID {{ serviceID }}
                    with Professional whose ID is {{ professionalID }}?
                </h2>
                <form class="form-control mt-4">
                    <div class="flex items-center justify-center gap-4">
                        <button @click.prevent="onBookClick" class="btn btn-block btn-error">BOOK</button>
                    </div>
                </form>
                <!-- <p class="text-center text-lg font-bold">Requested Service Request Not Found</p> -->

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'customer_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </div>
</template>