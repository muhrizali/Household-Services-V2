<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getAPI } from '@/httpreqs';
const route = useRoute();
const professionalID = route.params.id;

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
                <table class="table table-sm">
                    <tbody>
                        <tr>
                            <td class="text-lg font-bold">ID:</td>
                            <td>{{ professional.id }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">NAME:</td>
                            <td>{{ professional.user.fullname }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">USERNAME:</td>
                            <td>{{ professional.user.username }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">SERVICE:</td>
                            <td>{{ professional.service.name }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">EXPERIENCE:</td>
                            <td>{{ professional.experience }} Years</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">APPROVAL:</td>
                            <td>
                                <span v-if="professional.approval === 'REJECTED'" class="badge badge-lg badge-error">{{
                                    professional.approval }}</span>
                                <span v-else-if="professional.approval === 'PENDING'"
                                    class="badge badge-lg border-dashed">{{
                                        professional.approval }}</span>
                                <span v-else class="badge badge-lg badge-success">{{ professional.approval }}</span>
                            </td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">AVERAGE RATING:</td>
                            <td>{{ professional.avg_rating }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">EMAIL:</td>
                            <td>{{ professional.user.email }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">CONTACT:</td>
                            <td>{{ professional.contact }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">ADDRESS:</td>
                            <td>{{ professional.address }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">PIN CODE:</td>
                            <td>{{ professional.pincode }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">DESCRIPTION:</td>
                            <td>{{ professional.description }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold">CREATED:</td>
                            <td>{{ professional.created }}</td>
                        </tr>
                    </tbody>
                </table>

                <!-- Professional Actions -->
                <span class="flex justify-end gap-2">
                    <RouterLink :to="{ name: 'admin_professional_approve', params: { id: professional.id } }">
                        <button class="btn btn-sm btn-success">👍 APPROVE</button>
                    </RouterLink>
                    <RouterLink :to="{ name: 'admin_professional_reject', params: { id: professional.id } }">
                        <button class="btn btn-sm btn-error">👎 REJECT</button>
                    </RouterLink>
                </span>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested Professional Not Found</p>
            </div>
            <p class="text-center text-lg font-bold">{{ message }}</p>
            <!-- {{ professional }} -->


            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'admin_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </section>
</template>