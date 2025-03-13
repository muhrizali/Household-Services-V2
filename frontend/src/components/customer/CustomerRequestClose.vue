<script setup>
import { getAPI, putAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const serviceRequestID = route.params.rid;

const serviceRequestFound = ref(false);
const serviceRequest = ref({});
const message = ref('');

const rating = ref(0);
const remarks = ref('');

function serviceRequestEditData() {
    return {
        'id': serviceRequestID,
        'rating': rating.value,
        'remarks': remarks.value,
        'close_request': true,
    }
}

async function initialLoad() {
    const response = await getAPI({ url: '/api/request', params: { 'id': serviceRequestID } });
    if (response.data.found) {
        serviceRequestFound.value = true;
        serviceRequest.value = response.data.service_request;
    } else {
        message.value = 'Service Request not found';
    }
}

async function onSubmitClick() {
    const response = await putAPI({ url: '/api/request', data: serviceRequestEditData() });
    if (response.data.edited) {
        message.value = 'Service Request successfully closed';
    } else {
        message.value = 'Some error occured';
    }

}

const selectRatings = [
    {
        value: 1,
        name: '⭐'
    },
    {
        value: 2,
        name: '⭐⭐'
    },
    {
        value: 3,
        name: '⭐⭐⭐'
    },
    {
        value: 4,
        name: '⭐⭐⭐⭐'
    },
    {
        value: 5,
        name: '⭐⭐⭐⭐⭐'
    },
];

onMounted(initialLoad);

</script>
<template>
    <section class="w-2/3 card card-bordered border-2">
        <div class="card-body">
            <!-- FLASH MESSAGES -->
            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                {{ message }}
            </div>
            <div v-if="serviceRequestFound">
                <h2 class="card-title text-lg">CLOSING SERVICE?</h2>
                <table class="table">
                    <tbody>
                        <tr>
                            <td class="text-lg font-bold underline">REQUEST ID:</td>
                            <td>{{ serviceRequest.id }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">NAME:</td>
                            <td>{{ serviceRequest.service.name }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">DESCRIPTION:</td>
                            <td>{{ serviceRequest.service.description }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">PRICE:</td>
                            <td>{{ serviceRequest.service.price }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">REQUESTED:</td>
                            <td>{{ serviceRequest.created }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">PROFESSIONAL ID:</td>
                            <td>{{ serviceRequest.professional.id }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">PROFESSIONAL:</td>
                            <td>{{ serviceRequest.professional.user.fullname }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">CONTACT:</td>
                            <td>{{ serviceRequest.professional.contact }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                <p class="text-xl text-center font-medium">Service Request History not found</p>
            </div>
        </div>
    </section>

    <!-- Rating and Remarks Form -->
    <section class="w-2/3 card card-bordered border-2">
        <div class="card-body">
            <h2 class="card-title text-lg">Rate Us!</h2>
            <form class="card-body form-control">
                <table class="table">
                    <!-- Selecting Service Type from DB -->
                    <tr>
                        <td class="text-lg font-bold underline">
                            <label for="rating">RATING:</label>
                        </td>
                        <td>
                            <select v-model="rating" id="rating" class="select w-full select-bordered">
                                <option value='0'>--- SELECT ONE ---</option>
                                <option v-for="rate in selectRatings" :value="rate.value">{{ rate.name }}</option>
                            </select>
                        </td>
                    </tr>

                    <tr>
                        <td class="text-lg font-bold underline">
                            <label for="remarks">REMARKS (if any):</label>
                        </td>
                        <td>
                            <textarea placeholder="Your Experience With Us" v-model="remarks" id="remarks"
                                class="textarea w-full textarea-bordered">
                            </textarea>
                        </td>
                    </tr>
                </table>

                <!-- Rating Actions -->
                <div class="flex items-center justify-end gap-4">
                    <button @click.prevent="onSubmitClick" class="btn btn-lg btn-block btn-success">SUBMIT</button>
                </div>
            </form>

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'customer_home' }" class="link link-primary">Home</RouterLink>
            </p>

        </div>
    </section>
</template>