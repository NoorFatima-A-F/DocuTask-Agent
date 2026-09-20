import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { OrganizationNode } from '../../types/saasPlatform';
import { Network, Building, FolderTree, MapPin, RefreshCw } from 'lucide-react';

export const OrganizationManager: React.FC = () => {
  const [tree, setTree] = useState<OrganizationNode[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTree = async () => {
      setLoading(true);
      const data = await SaaSApiClient.getOrganizationTree('tenant_acme_corp');
      setTree(data);
      setLoading(false);
    };
    fetchTree();
  }, []);

  const renderNode = (node: OrganizationNode, depth = 0) => (
    <div key={node.organization_id} className="space-y-3" style={{ marginLeft: `${depth * 24}px` }}>
      <div className="p-4 rounded-lg bg-slate-800/60 border border-slate-700 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Building className="w-5 h-5 text-indigo-400" />
          <div>
            <span className="text-sm font-semibold text-white block">{node.name}</span>
            <span className="text-xs text-slate-400">{node.business_unit} • {node.organization_id}</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="outline" className="flex items-center gap-1 text-xs">
            <MapPin className="w-3 h-3" /> {node.country_code}
          </Badge>
          <Badge variant="info">Org Node</Badge>
        </div>
      </div>
      {node.children && node.children.map((child) => renderNode(child, depth + 1))}
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Network className="w-7 h-7 text-indigo-400" />
            Enterprise Organization Hierarchy
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Hierarchical multi-level structure: Tenant → Divisions → Business Units → Labs.
          </p>
        </div>
        <Badge variant="intelligence" className="px-3 py-1">
          <FolderTree className="w-4 h-4 mr-1 inline" /> Tree View
        </Badge>
      </div>

      <Card className="bg-slate-900/80 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white">Acme Corporation Global Division Tree</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {loading ? (
            <div className="p-8 text-center text-slate-400">
              <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading hierarchy...
            </div>
          ) : (
            tree.map((root) => renderNode(root))
          )}
        </CardContent>
      </Card>
    </div>
  );
};
