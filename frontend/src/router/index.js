import { createRouter, createWebHistory } from 'vue-router';
import LoginForm from '@/components/LoginForm.vue';
import CustomerRegisterForm from '@/components/CustomerRegisterForm.vue';
import ProfessionalRegisterForm from '@/components/ProfessionalRegisterForm.vue';
import AdminHome from '@/components/admin/AdminHome.vue';
import Testing from '@/components/Testing.vue';
import DashboardView from '@/views/DashboardView.vue';
import LandingHomeView from '@/views/LandingHomeView.vue';
import CustomerHome from '@/components/customer/CustomerHome.vue';
import ProfessionalHome from '@/components/professionals/ProfessionalHome.vue';
import AdminServiceDetails from '@/components/admin/AdminServiceDetails.vue';
import AdminProfessionalDetails from '@/components/admin/AdminProfessionalDetails.vue';
import AdminCustomerDetails from '@/components/admin/AdminCustomerDetails.vue';
import AdminRequestDetails from '@/components/admin/AdminRequestDetails.vue';
import AdminServiceCreate from '@/components/admin/AdminServiceCreate.vue';
import AdminServiceDelete from '@/components/admin/AdminServiceDelete.vue';
import AdminServiceEdit from '@/components/admin/AdminServiceEdit.vue';
import AdminProfessionalApprove from '@/components/admin/AdminProfessionalApprove.vue';
import AdminProfessionalReject from '@/components/admin/AdminProfessionalReject.vue';
import AdminCustomerActivate from '@/components/admin/AdminCustomerActivate.vue';
import AdminCustomerBlock from '@/components/admin/AdminCustomerBlock.vue';
import AdminDashboardView from '@/views/AdminDashboardView.vue';
import AdminRequestEdit from '@/components/admin/AdminRequestEdit.vue';
import AdminRequestDelete from '@/components/admin/AdminRequestDelete.vue';
import AdminSearch from '@/components/admin/AdminSearch.vue';
import CustomerDashboardView from '@/views/CustomerDashboardView.vue';
import CustomerProfileDetails from '@/components/customer/CustomerProfileDetails.vue';
import CustomerRequestDetails from '@/components/customer/CustomerRequestDetails.vue';
import CustomerRequestCancel from '@/components/customer/CustomerRequestCancel.vue';
import CustomerServiceDetails from '@/components/customer/CustomerServiceDetails.vue';
import CustomerProfessionalDetails from '@/components/customer/CustomerProfessionalDetails.vue';
import CustomerRequestBook from '@/components/customer/CustomerRequestBook.vue';
import CustomerRequestClose from '@/components/customer/CustomerRequestClose.vue';
import CustomerProfileEdit from '@/components/customer/CustomerProfileEdit.vue';
import CustomerSearch from '@/components/customer/CustomerSearch.vue';
import ProfessionalDashboardView from '@/views/ProfessionalDashboardView.vue';
import ProfessionalSearch from '@/components/professionals/ProfessionalSearch.vue';
import ProfessionalProfileDetails from '@/components/professionals/ProfessionalProfileDetails.vue';
import ProfessionalProfileEdit from '@/components/professionals/ProfessionalProfileEdit.vue';
import ProfessionalRequestDetails from '@/components/professionals/ProfessionalRequestDetails.vue';
import ProfessionalRequestAccept from '@/components/professionals/ProfessionalRequestAccept.vue';
import ProfessionalRequestReject from '@/components/professionals/ProfessionalRequestReject.vue';
import AccessNotAllowed from '@/components/AccessNotAllowed.vue';
import AdminReports from '@/components/admin/AdminReports.vue';
// import HomeView from '../views/HomeView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: LandingHomeView,
      children: [
        {
          path: "",
          component: LoginForm
        },
        {
          path: "login",
          name: "login",
          component: LoginForm,
        },
        {
          path: "access-not-allowed",
          name: "access_not_allowed",
          component: AccessNotAllowed,
        },
      ]
    },
    {
      path: '/register',
      component: LandingHomeView,
      children: [
        {
          path: "customer",
          name: "customer_register",
          component: CustomerRegisterForm
        },
        {
          path: "professional",
          name: "professional_register",
          component: ProfessionalRegisterForm
        }
      ]
    },
    {
      path: "/user",
      children: [
        {
          path: "admin",
          component: AdminDashboardView,
          children: [
            {
              path: "",
              name: "admin_home",
              component: AdminHome
            },
            {
              path: "search/",
              name: "admin_search",
              component: AdminSearch
            },
            {
              path: "report/",
              name: "admin_reports",
              component: AdminReports
            },
            {
              path: "service/details/:id",
              name: "admin_service_details",
              component: AdminServiceDetails
            },
            {
              path: "service/create",
              name: "admin_service_create",
              component: AdminServiceCreate
            },
            {
              path: "service/delete/:id",
              name: "admin_service_delete",
              component: AdminServiceDelete
            },
            {
              path: "service/edit/:id",
              name: "admin_service_edit",
              component: AdminServiceEdit
            },
            {
              path: "professional/details/:id",
              name: "admin_professional_details",
              component: AdminProfessionalDetails
            },
            {
              path: "professional/approve/:id",
              name: "admin_professional_approve",
              component: AdminProfessionalApprove
            },
            {
              path: "professional/reject/:id",
              name: "admin_professional_reject",
              component: AdminProfessionalReject
            },
            {
              path: "customer/details/:id",
              name: "admin_customer_details",
              component: AdminCustomerDetails
            },
            {
              path: "customer/activate/:id",
              name: "admin_customer_activate",
              component: AdminCustomerActivate
            },
            {
              path: "customer/block/:id",
              name: "admin_customer_block",
              component: AdminCustomerBlock
            },
            {
              path: "request/details/:id",
              name: "admin_request_details",
              component: AdminRequestDetails
            },
            {
              path: "request/edit/:id",
              name: "admin_request_edit",
              component: AdminRequestEdit
            },
            {
              path: "request/delete/:id",
              name: "admin_request_delete",
              component: AdminRequestDelete
            },
          ]
        },
        {
          path: "customer/:id",
          component: CustomerDashboardView,
          children: [
            {
              path: "",
              name: "customer_home",
              component: CustomerHome,
            },
            {
              path: "search",
              name: "customer_search",
              component: CustomerSearch,
            },
            {
              path: "profile",
              name: "customer_profile_details",
              component: CustomerProfileDetails,
            },
            {
              path: "edit",
              name: "customer_profile_edit",
              component: CustomerProfileEdit,
            },
            {
              path: "service/:sid",
              name: "customer_service_details",
              component: CustomerServiceDetails,
            },
            {
              path: "service/:sid/professional/:pid",
              name: "customer_professional_details",
              component: CustomerProfessionalDetails,
            },
            {
              path: "service/:sid/professional/:pid/book",
              name: "customer_request_book",
              component: CustomerRequestBook,
            },
            {
              path: "request/:rid",
              name: "customer_request_details",
              component: CustomerRequestDetails,
            },
            {
              path: "request/cancel/:rid",
              name: "customer_request_cancel",
              component: CustomerRequestCancel,
            },
            {
              path: "request/close/:rid",
              name: "customer_request_close",
              component: CustomerRequestClose,
            },
          ]
        },
        {
          path: "professional/:id",
          component: ProfessionalDashboardView,
          children: [
            {
              path: "",
              name: "professional_home",
              component: ProfessionalHome,
            },
            {
              path: "search",
              name: "professional_search",
              component: ProfessionalSearch,
            },
            {
              path: "profile",
              name: "professional_profile_details",
              component: ProfessionalProfileDetails,
            },
            {
              path: "edit",
              name: "professional_profile_edit",
              component: ProfessionalProfileEdit,
            },
            {
              path: "request/:rid",
              name: "professional_request_details",
              component: ProfessionalRequestDetails,
            },
            {
              path: "request/accept/:rid",
              name: "professional_request_accept",
              component: ProfessionalRequestAccept,
            },
            {
              path: "request/reject/:rid",
              name: "professional_request_reject",
              component: ProfessionalRequestReject,
            },
          ]
        },
      ]
    },
    {
      path: "/testing",
      name: "testing",
      component: Testing
    }
  ],
});

export default router;
