import React from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import useSWR from "swr";
import { observer } from "mobx-react-lite";
// mobx store
import { useMobxStore } from "lib/mobx/store-provider";
// layouts
import { AppLayout } from "layouts/app-layout";
import { WorkspaceSettingLayout } from "layouts/settings-layout";
// components
import { WorkspaceSettingHeader } from "components/headers";
import { WebhooksList, WebhooksEmptyState } from "components/web-hooks";
// ui
import { Button, Spinner } from "@plane/ui";
// types
import { NextPageWithLayout } from "types/app";

const WebhooksListPage: NextPageWithLayout = observer(() => {
  const router = useRouter();
  const { workspaceSlug } = router.query;

  const {
    webhook: { fetchWebhooks, webhooks },
    user: { currentWorkspaceRole },
  } = useMobxStore();

  const isAdmin = currentWorkspaceRole === 20;

  useSWR(
    workspaceSlug && isAdmin ? `WEBHOOKS_LIST_${workspaceSlug}` : null,
    workspaceSlug && isAdmin ? () => fetchWebhooks(workspaceSlug.toString()) : null
  );

  if (!isAdmin)
    return (
      <div className="mt-10 flex h-full w-full justify-center p-4">
        <p className="text-sm text-custom-text-300">You are not authorized to access this page.</p>
      </div>
    );

  if (!webhooks)
    return (
      <div className="grid h-full w-full place-items-center p-4">
        <Spinner />
      </div>
    );

  return (
    <div className="h-full w-full overflow-hidden py-8 pr-9">
      {Object.keys(webhooks).length > 0 ? (
        <div className="flex h-full w-full flex-col">
          <div className="flex items-center justify-between gap-4 border-b border-custom-border-200 pb-3.5">
            <div className="text-xl font-medium">Webhooks</div>
            <Link href={`/${workspaceSlug}/settings/webhooks/create`}>
              <Button variant="primary" size="sm">
                Add webhook
              </Button>
            </Link>
          </div>
          <WebhooksList />
        </div>
      ) : (
        <div className="mx-auto">
          <WebhooksEmptyState />
        </div>
      )}
    </div>
  );
});

WebhooksListPage.getLayout = function getLayout(page: React.ReactElement) {
  return (
    <AppLayout header={<WorkspaceSettingHeader title="Webhook settings" />}>
      <WorkspaceSettingLayout>{page}</WorkspaceSettingLayout>
    </AppLayout>
  );
};

export default WebhooksListPage;
