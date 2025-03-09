<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getAPI, putAPI } from '@/httpreqs';
const route = useRoute();
const serviceRequestID = route.params.id;

const serviceRequest = ref({});
const serviceRequestFound = ref(false);
const message = ref("");


const status = ref("");
const rating = ref(0);
const stars = ref("");
const remarks = ref("");
const completed = ref("");

async function initialLoad() {
    try {
        const response = await getAPI({ url: "/api/request", params: { "id": serviceRequestID } });
        if (response.data.found) {
            serviceRequestFound.value = true;
            serviceRequest.value = response.data.service_request;

            status.value = serviceRequest.value.status;
            rating.value = serviceRequest.value.rating;
            stars.value = "⭐".repeat(rating.value);
            remarks.value = serviceRequest.value.remarks;
            completed.value = serviceRequest.value.completed;
        } else {
            serviceRequestFound.value = false;
        }
    } catch (error) {
        message.value = "Something Went Wrong";
    }
}

function serviceRequestEditData() {
    return {
        "id": serviceRequestID,
        "remarks": remarks.value,
        "completed": completed.value,
    };
}

async function onEditClick() {
    try {
        const response = await putAPI({ url: "/api/request", data: serviceRequestEditData() });
        if (response.data.edited) {
            message.value = "Service Request Successfully Updated";
        } else {
            message.value = "Service Request Could Not be Updated";
        }
    } catch {
        message.value = "Error Occured while Updating Service Request";
    }
    setTimeout(function () {
        message.value = "";
    }, 2000);
}

onMounted(initialLoad);

</script>
<template>
    <div class="flex items-center justify-center w-full h-fit m-8">
        <div class="card card-bordered border-2 border-primary-content/25 w-2/3">
            <div class="card-body">
                <h2 class="card-title text-lg">EDIT SERVICE REQUEST</h2>
                <!-- {{ serviceRequest }} -->

                <div v-show="message"
                    class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                    {{ message }}
                </div>

                <div v-if="serviceRequestFound">
                    <form class="form-control">
                        <table class="table table-sm">
                            <tbody>
                                <tr>
                                    <td>
                                        <label for="service_name">SERVICE:</label>
                                    </td>
                                    <td>
                                        {{ serviceRequest.service.name }}
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="professional_name">PROFESSIONAL:</label>
                                    </td>
                                    <td>
                                        {{ serviceRequest.professional.user.fullname }}
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="customer_name">CUSTOMER:</label>
                                    </td>
                                    <td>
                                        {{ serviceRequest.customer.user.fullname }}
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="status">STATUS:</label>
                                    </td>
                                    <td>
                                        <span v-if="status === 'REQUESTED'"
                                            class="badge badge-lg badge-error">REQUESTED</span>
                                        <span v-else-if="status === 'ASSIGNED'"
                                            class="badge badge-lg badge-warning">ASSIGNED</span>
                                        <span v-else class="badge badge-lg badge-success">CLOSED</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="rating">RATING:</label>
                                    </td>
                                    <td>
                                        {{ rating }}/5 [{{ stars }}]
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="remarks">REMARKS:</label>
                                    </td>
                                    <td>
                                        <textarea name="remarks" id="remarks"
                                            class="textarea w-full textarea-bordered border-2" rows="4"
                                            v-model="remarks"></textarea>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="completed">COMPLETED:</label>
                                    </td>
                                    <td>
                                        <input type="text" id="completed" class="input w-full input-bordered border-2"
                                            v-model="completed">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="flex items-center justify-center mt-4">
                            <button @click.prevent="onEditClick" class="btn btn-block btn-lg btn-warning">EDIT</button>
                        </div>
                    </form>
                </div>
                <div v-else>
                    <p class="text-center text-lg font-bold">Requested Service Request not be Edited</p>
                </div>

                <p class="text-center pt-2">
                    Go back to <RouterLink :to="{ name: 'admin_home' }" class="link link-primary">Home</RouterLink>
                </p>
            </div>
        </div>
    </div>
</template>