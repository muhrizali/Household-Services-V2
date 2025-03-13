<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getAPI } from '@/httpreqs';

const route = useRoute();
const serviceID = route.params.sid;
const professionalID = route.params.pid;

const professional = ref({});
const professionalFound = ref(false);
const message = ref("");

onMounted(async function () {
    try {
        const response = await getAPI({ url: "/api/professional", params: { "id": professionalID } });
        if (response.data.found) {
            professionalFound.value = true;
            professional.value = response.data.professional;
        } else {
            professionalFound.value = false;
        }
    } catch (error) {
        message.value = `Something Went Wrong; ${error}`;
    }
})

</script>
<template>
    <section class="w-2/3 card card-bordered border-2">
        <div class="card-body">
            <div v-if="professionalFound">
                <h2 class="card-title text-lg">PROFESSIONAL DETAILS:</h2>
                <table class="table table-lg">
                    <tbody>
                        <tr>
                            <td class="text-lg font-bold underline">ID:</td>
                            <td>{{ professional.id }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">NAME:</td>
                            <td>{{ professional.user.fullname }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">USERNAME:</td>
                            <td>{{ professional.user.username }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">SERVICE:</td>
                            <td>{{ professional.service.name }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">AVERAGE RATING:</td>
                            <td>{{ professional.avg_rating }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">EMAIL:</td>
                            <td>{{ professional.user.email }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">CONTACT:</td>
                            <td>{{ professional.contact }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">ADDRESS:</td>
                            <td>{{ professional.address }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">PIN CODE:</td>
                            <td>{{ professional.pincode }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">EXPERIENCE:</td>
                            <td>{{ professional.experience }} Years</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">DESCRIPTION:</td>
                            <td>{{ professional.description }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">CREATED:</td>
                            <td>{{ professional.created }}</td>
                        </tr>
                    </tbody>
                </table>

                <!-- Professional Actions -->
                <span class="flex justify-end gap-2">
                    <RouterLink :to="{ name: 'customer_request_book', params: { sid: serviceID, pid: professionalID } }">
                        <button class="btn btn-sm btn-success">BOOK</button>
                    </RouterLink>
                </span>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested Professional Not Found</p>
            </div>
            <p class="text-center text-lg font-bold">{{ message }}</p>

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'customer_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </section>
</template>