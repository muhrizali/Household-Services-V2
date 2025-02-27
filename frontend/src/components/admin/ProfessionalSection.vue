<script setup>
import { onMounted, ref } from 'vue';
import { getAPI } from '@/httpreqs';
const professionals = ref([]);

onMounted(async function () {
    const response = await getAPI({ url: "/api/professional" });
    professionals.value = response.data.professionals;
})
</script>
<template>
    <!-- Professional List Table -->
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">PROFESSIONALS</h2>
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>NAME</th>
                        <th>SERVICE</th>
                        <th>RATING</th>
                        <th>STATUS</th>
                        <th>APPLIED</th>
                        <th>ACTIONS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="professionals.length" v-for="prof in professionals" :key="prof.id">
                        <td>
                            <RouterLink :to="{ name: 'admin_professional_details', params: { id: prof.id } }">
                                <button class="btn btn-sm">{{ prof.id }}</button>
                            </RouterLink>
                        </td>
                        <td>{{ prof.user.fullname }}</td>
                        <td>{{ prof.service.name }}</td>
                        <td>{{ prof.avg_rating }}</td>
                        <td>
                            <span v-if="prof.approval === 'REJECTED'" class="badge badge-lg badge-error">{{ prof.approval }}</span>
                            <span v-else-if="prof.approval === 'PENDING'" class="badge badge-lg border-dashed">{{ prof.approval }}</span>
                            <span v-else class="badge badge-lg badge-success">{{ prof.approval }}</span>
                        </td>
                        <td>{{ prof.created }}</td>
                        <td>
                            <span>
                                <a href="">
                                    <button class="btn btn-sm btn-success">Approve</button>
                                </a>
                                <a href="">
                                    <button class="btn btn-sm btn-error">Reject</button>
                                </a>
                            </span>
                        </td>
                    </tr>
                    <tr v-else>
                        <td colspan="7" class="text-center font-bold text-error-content text-lg">No Professionals Found
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
</template>