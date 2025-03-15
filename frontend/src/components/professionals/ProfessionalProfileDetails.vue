<script setup>
import { getAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();

const professionalID = route.params.id;

const professionalFound = ref(false);
const professional = ref({});

const message = ref('');

async function initialLoad() {
  const response = await getAPI({ url: '/api/professional', params: { 'id': professionalID } });
  if (response.data.found) {
    professionalFound.value = true;
    professional.value = response.data.professional;
  } else {
    message.value = 'Professional Not Found';
  }
}

onMounted(initialLoad);

</script>
<template>
    <section class="w-2/3 card card-bordered border-2">
        <div class="card-body">
            <div v-if="professionalFound">
                <h2 class="card-title text-lg">PROFESSIONAL DETAILS:</h2>
                <table class="table table-sm">
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
                            <td class="text-lg font-bold underline">EMAIL:</td>
                            <td>{{ professional.user.email }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">CONTACT:</td>
                            <td>{{ professional.contact }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">SERVICE:</td>
                            <td>{{ professional.service.name }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">EXPERIENCE:</td>
                            <td>{{ professional.experience }} Years</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">RATING:</td>
                            <td>{{ professional.avg_rating }}</td>
                        </tr>
                        <tr>
                            <td class="text-lg font-bold underline">STATUS:</td>
                            <td>{{ professional.approval }}</td>
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
                            <td class="text-lg font-bold underline">JOINED:</td>
                            <td>{{ professional.created }}</td>
                        </tr>
                    </tbody>
                </table>
                <!-- Customer Actions -->
                <div class="flex items-center justify-end gap-2">
                    <RouterLink :to="{ name: 'professional_profile_edit' }">
                        <button class="btn btn-sm btn-primary">EDIT</button>
                    </RouterLink>
                </div>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested professional not found</p>
            </div>

            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'professional_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>
    </section>
</template>