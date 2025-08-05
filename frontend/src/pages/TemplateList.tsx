import React, { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "../hooks/redux";
import { fetchTemplates } from "../store/templateSlice";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { useScreenshotDetection } from "../hooks/useScreenshotDetection";
import { useNavigate } from "react-router-dom";

const TemplateList: React.FC = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { templates, loading, error } = useAppSelector(
    (state) => state.templates
  );
  useScreenshotDetection(); // Hook to detect screenshots

  useEffect(() => {
    dispatch(fetchTemplates());
  }, [dispatch]);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-extrabold text-gray-900 mb-6">
          Available Templates
        </h2>

        {loading && <Loading />}
        {error && (
          <ErrorMessage
            message={error}
            onRetry={() => dispatch(fetchTemplates())}
          />
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map((template) => (
            <div
              key={template._id}
              className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden"
            >
              <img
                src={template.image_url}
                alt={template.title}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <h5 className="text-lg font-semibold text-gray-900">
                  {template.title}
                </h5>
                <p className="text-sm text-gray-600 mt-1">
                  {template.description}
                </p>
                <button
                  className="mt-4 w-full bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium py-2 px-4 border border-transparent rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  onClick={() => navigate("/payment")}
                >
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TemplateList;
