using UnityEngine;
using Live2D.Cubism.Core;
using System.Collections.Generic;

public class Live2DController : MonoBehaviour
{
    public CubismModel model;

    private Dictionary<string, CubismParameter> paramDict;

    void Start()
    {
        if (model == null)
        {
            Debug.LogError("CubismModel is NULL!");
            return;
        }

        paramDict = new Dictionary<string, CubismParameter>();

        foreach (var p in model.Parameters)
        {
            if (!paramDict.ContainsKey(p.Id))
                paramDict.Add(p.Id, p);
        }

        Debug.Log($"Live2DController initialized. Param count = {paramDict.Count}");
    }

    void SetParam(string id, float value)
    {
        if (paramDict == null) return;
        if (!paramDict.ContainsKey(id)) return;

        paramDict[id].Value = value;
    }

    void Update()
    {
        if (model == null) return;
        if (paramDict == null) return;
        if (string.IsNullOrEmpty(UDPReceiver.data)) return;

        FaceData d = JsonUtility.FromJson<FaceData>(UDPReceiver.data);
        if (d == null) return;

        // ===== HEAD =====
        SetParam("ParamAngleX", d.headX);
        SetParam("ParamAngleY", d.headY);

        // ===== EYES =====
        SetParam("ParamEyeBallX", d.eyeX);
        SetParam("ParamEyeBallY", d.eyeY);
        SetParam("ParamEyeLOpen", d.eyeLOpen);
        SetParam("ParamEyeROpen", d.eyeROpen);

        // ===== MOUTH =====
        float m = Mathf.Clamp01(d.mouth);

        // Bibir atas naik
        SetParam("ParamMouthUp", m);

        // Bibir bawah turun (arah kebalikan)
        SetParam("ParamMouthDown", -m);

        SetParam("ParamBodyAngleX", d.bodyX);
        SetParam("ParamBodyAngleY", d.bodyY);
        SetParam("ParamBodyAngleZ", d.bodyZ);

        // LEFT ARM
        SetParam("ParamArmLA01", d.armL * 0.4f);
        SetParam("ParamArmLA02", d.armL * 0.3f);
        SetParam("ParamArmLA03", d.armL * 0.2f);
        SetParam("ParamHandLA", d.armL * 0.5f);

        // RIGHT ARM
        SetParam("ParamArmRA01", d.armR * 0.4f);
        SetParam("ParamArmRA02", d.armR * 0.3f);
        SetParam("ParamArmRA03", d.armR * 0.2f);
        SetParam("ParamHandRA", d.armR * 0.5f);


    }
}
