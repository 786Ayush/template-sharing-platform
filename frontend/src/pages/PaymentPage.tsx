import React from 'react';
import { Link } from 'react-router-dom';

const PaymentPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
            <svg
              className="h-6 w-6 text-red-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
              />
            </svg>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Screenshot Detected!
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            To download or take screenshots of our premium templates, please make a payment.
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Pricing Plans
          </h3>
          
          <div className="space-y-4">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="text-md font-semibold text-gray-900">Single Template</h4>
              <p className="text-2xl font-bold text-primary-600">$9.99</p>
              <p className="text-sm text-gray-600">Access to one template</p>
              <button className="mt-2 w-full bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium py-2 px-4 border border-transparent rounded-md">
                Pay Now
              </button>
            </div>

            <div className="border border-primary-200 rounded-lg p-4 bg-primary-50">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="text-md font-semibold text-gray-900">Premium Access</h4>
                  <p className="text-2xl font-bold text-primary-600">$29.99</p>
                  <p className="text-sm text-gray-600">Access to all templates</p>
                </div>
                <span className="bg-primary-600 text-white text-xs px-2 py-1 rounded">Popular</span>
              </div>
              <button className="mt-2 w-full bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium py-2 px-4 border border-transparent rounded-md">
                Pay Now
              </button>
            </div>

            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="text-md font-semibold text-gray-900">Monthly Subscription</h4>
              <p className="text-2xl font-bold text-primary-600">$19.99<span className="text-sm text-gray-600">/month</span></p>
              <p className="text-sm text-gray-600">Unlimited access + new templates</p>
              <button className="mt-2 w-full bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium py-2 px-4 border border-transparent rounded-md">
                Subscribe
              </button>
            </div>
          </div>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-500">
              Secure payment powered by Stripe
            </p>
          </div>
        </div>

        <div className="text-center">
          <Link
            to="/templates"
            className="font-medium text-primary-600 hover:text-primary-500"
          >
            ← Back to Templates
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PaymentPage;
