import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { Subscription, Invoice } from '../../types/saasPlatform';
import { CreditCard, CheckCircle2, Receipt, ArrowUpRight, RefreshCw } from 'lucide-react';

export const SubscriptionBillingConsole: React.FC = () => {
  const [subs, setSubs] = useState<Subscription[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const [s, inv] = await Promise.all([
        SaaSApiClient.listSubscriptions(),
        SaaSApiClient.listInvoices('tenant_acme_corp'),
      ]);
      setSubs(s);
      setInvoices(inv);
      setLoading(false);
    };
    load();
  }, []);

  const activeSub = subs.find((s) => s.tenant_id === 'tenant_acme_corp') || subs[0];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <CreditCard className="w-7 h-7 text-indigo-400" />
            Subscription & Invoicing Gateway
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Enterprise plans, recurring billing schedules, Stripe/Paddle gateways, and invoice ledgers.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Billing Data...
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Active Plan Card */}
          <Card className="bg-slate-900/80 border-slate-800 lg:col-span-1">
            <CardHeader>
              <CardTitle className="text-base text-white">Current Enterprise Plan</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-4 bg-gradient-to-br from-indigo-950/40 to-slate-900 border border-indigo-800/40 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-xl font-bold text-white">{activeSub?.tier} PLAN</span>
                  <Badge variant="intelligence">{activeSub?.billing_interval}</Badge>
                </div>
                <div className="mt-3">
                  <span className="text-3xl font-extrabold text-white">${activeSub?.base_price_monthly_usd}</span>
                  <span className="text-xs text-slate-400"> / month</span>
                </div>
              </div>

              <div className="space-y-2 text-xs text-slate-300">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Unlimited Autonomous Agent Meshes
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" /> 1 Billion Tokens / Month included
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Multi-Region Isolated Sandbox
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" /> 24/7 Dedicated SLA & SOC2 Compliance
                </div>
              </div>

              <Button variant="intelligence" className="w-full">
                <span className="flex items-center justify-center gap-2">
                  <ArrowUpRight className="w-4 h-4" /> Manage Subscription
                </span>
              </Button>
            </CardContent>
          </Card>

          {/* Invoices */}
          <Card className="bg-slate-900/80 border-slate-800 lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-base text-white flex items-center gap-2">
                <Receipt className="w-5 h-5 text-emerald-400" /> Invoice History & Payment Status
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {invoices.map((inv) => (
                <div
                  key={inv.invoice_id}
                  className="p-4 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between"
                >
                  <div>
                    <span className="text-sm font-semibold text-white block">{inv.invoice_id}</span>
                    <span className="text-xs text-slate-400">Period: {inv.billing_period} • Created: {new Date(inv.created_at).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-base font-bold text-white">${inv.amount_due_usd.toLocaleString()}</span>
                    <Badge variant={inv.status === 'PAID' ? 'success' : 'warning'}>{inv.status}</Badge>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
