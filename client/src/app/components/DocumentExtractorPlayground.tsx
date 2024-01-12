"use client";

import { init, Form } from "@feathery/react";
import { useEffect, useState } from "react";
import { submit } from "../actions";
import { ArrowTrendingUpIcon } from "@heroicons/react/20/solid";

export function DocumentExtractorPlayground() {
  // This is my test SDK key, the associated account will eventually be deleted.
  init("612fd85c-986d-4008-816b-6e2c7ad645c8");

  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [results, setResults] = useState<null | {
    account_owner_name: string;
    portfolio_value: string;
    holdings: {
      name: string | null;
      cost_basis: string | null;
      account: string | null;
    }[];
  }>(null);

  const FILE_UPLOAD_KEY = "please_upload_y-JJ";

  async function extract() {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("pdf_file", file);
    setResults(await submit(formData));
    setLoading(false);
  }

  function renderForm() {
    return (
      <div className="flex flex-col items-center justify-center">
        <Form
          formName="investment_statements"
          onChange={(ctx) => {
            let filePromises = ctx.getFieldValues()[FILE_UPLOAD_KEY];
            if (!Array.isArray(filePromises)) return;
            if (filePromises.length < 1) return;
            let filePromise = filePromises[0] as Promise<File>;
            filePromise.then(async (fulfilled) => {
              setFile(fulfilled);
            });
          }}
        />
        {file && (
          <button
            type="button"
            className="bg-rose-400 rounded-full p-5 text-white font-bold cursor-pointer w-[150px]"
            onClick={extract}
          >
            Extract
          </button>
        )}
      </div>
    );
  }

  function renderResults() {
    if (!results) return <></>;

    return (
      <div className="overflow-hidden bg-white shadow sm:rounded-lg w-full">
        <div className="px-4 py-6 sm:px-6 flex justify-between">
          <div>
            <h3 className="text-base font-semibold leading-7 text-gray-900">
              Applicant Information
            </h3>
            <p className="mt-1 max-w-2xl text-sm leading-6 text-gray-500">
              Details extracted from your uploaded file.
            </p>
          </div>
          <a
            type="button"
            className="font-medium text-rose-500 hover:text-rose-400 cursor-pointer"
            onClick={() => window.location.reload()}
          >
            + Extract New Document
          </a>
        </div>
        <div className="border-t border-gray-100">
          <dl className="divide-y divide-gray-100">
            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-900">
                Account Owner
              </dt>
              <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {results?.account_owner_name}
              </dd>
            </div>
            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-900">
                Portfolio Value
              </dt>
              <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {results?.portfolio_value}
              </dd>
            </div>
            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium leading-6 text-gray-900">
                Holdings
              </dt>
              <dd className="mt-2 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                <ul
                  role="list"
                  className="divide-y divide-gray-100 rounded-md border border-gray-200"
                >
                  {results?.holdings?.map((holding) => {
                    return (
                      <li
                        className="flex items-center justify-between py-4 pl-4 pr-5 text-sm leading-6"
                        key={
                          holding.name ||
                          `holding-${results?.holdings?.indexOf(holding)}`
                        }
                      >
                        <div className="flex w-0 flex-1 items-center">
                          <ArrowTrendingUpIcon
                            className="h-5 w-5 flex-shrink-0 text-gray-400"
                            aria-hidden="true"
                          />
                          <div className="ml-4 flex min-w-0 flex-1 gap-2">
                            <span className="truncate font-medium">
                              {holding.name ||
                                `holding-${results?.holdings?.indexOf(
                                  holding
                                )}`}
                            </span>
                            <span className="flex-shrink-0 text-gray-400">
                              Acct:{" "}
                              {holding.account ||
                                `holding-account-${results.holdings?.indexOf(
                                  holding
                                )}`}
                            </span>
                          </div>
                        </div>
                        <div className="ml-4 flex-shrink-0">
                          <p className="font-medium text-rose-500 hover:text-rose-400">
                            {holding?.cost_basis || "None"}
                          </p>
                        </div>
                      </li>
                    );
                  })}
                </ul>
              </dd>
            </div>
          </dl>
        </div>
      </div>
    );
  }

  function renderUI() {
    if (results) {
      return renderResults();
    }

    return renderForm();
  }

  if (loading) {
    return (
      <div className="bg-white shadow sm:rounded-lg text-center">
        <div className="px-4 py-5 sm:p-6 text-center">
          <h3 className="text-base font-semibold leading-6 text-gray-900">
            Extracting Data
          </h3>
          <div className="mt-2 max-w-xl text-sm text-gray-500">
            <p>
              Your file is being processed! Soon you'll be able to see
              structured data from {file?.name || "your file"}.
            </p>
            <p>This may take a while 🙂</p>
          </div>
          <div
            className="mt-5 inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite] text-rose-500"
            role="status"
          >
            <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
              Loading...
            </span>
          </div>
        </div>
      </div>
    );
  }

  return <>{renderUI()}</>;
}
